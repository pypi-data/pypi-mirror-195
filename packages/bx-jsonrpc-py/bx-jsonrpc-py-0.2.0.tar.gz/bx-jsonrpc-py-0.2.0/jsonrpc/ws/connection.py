import asyncio
import json
from asyncio import Future
from typing import (
    Optional,
    Any,
    NamedTuple,
    Callable,
    TypeVar,
    AsyncGenerator,
)

import websockets
import websockets.datastructures
from websockets import client as wsclient
from .response_queue import ResponseQueue
from .subscription_manager import SubscriptionManager, SubscriptionNotification
from ..types import (
    JsonRpcRequest,
    JsonRpcResponse,
    RpcMessageFormatException,
    RpcExecutionException,
)

T = TypeVar("T")


class WsRpcOpts(NamedTuple):
    encoder: Callable[[Any], str] = json.dumps
    decoder: Callable[[str], Any] = json.loads
    request_timeout_s: Optional[int] = 5
    notification_timeout_s: Optional[int] = None
    max_ws_size: int = 2**24
    headers: Optional[websockets.datastructures.HeadersLike] = None


class WsRpcConnection:
    """
    Wraps a websocket connection to serve as an RPC interface.

    Handles all reading and writing from a websockets RPC server with
    streaming as notifications support.

    Enhancement TODOs:
    - reconnection logic
    """

    uri: str
    opts: WsRpcOpts

    # internal state
    _ws: Optional[wsclient.WebSocketClientProtocol] = None
    _request_id: int = 1
    _subscription_manager: SubscriptionManager
    _response_queue: ResponseQueue

    # track tasks
    _receiver_task: Optional[Future] = None
    _status_task: Optional[Future] = None

    def __init__(self, uri: str, opts: Optional[WsRpcOpts] = None):
        if opts is None:
            opts = WsRpcOpts()

        self.uri = uri
        self.opts = opts

        self._subscription_manager = SubscriptionManager()
        self._response_queue = ResponseQueue()

    async def __aenter__(self) -> "WsRpcConnection":
        await self.connect()
        return self

    def __await__(self):
        yield from self.connect().__await__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        """
        Connects the websocket and creates all relevant tasks managing
        websocket message and statuses.
        """
        self._ws = await self.connect_ws()
        self._receiver_task = asyncio.create_task(self._read_loop())
        self._status_task = asyncio.create_task(self._ensure_ws())

    async def connect_ws(self) -> wsclient.WebSocketClientProtocol:
        return await websockets.connect(
            self.uri,
            max_size=self.opts.max_ws_size,
            extra_headers=self.opts.headers
        )

    async def call(
        self, method_name: str, params: Any, *, request_id: Optional[str] = None
    ) -> Any:
        """
        Executes an RPC call. Dispatches a method call with request ID to RPC
        server, and waits for the matching response. `call` times out based
        on the initial options configuration.

        :param method_name: method to call
        :param params: method parameters
        :param request_id: request ID to override (should be skipped in most cases)
        :return: RPC response
        """
        if request_id is None:
            request_id = str(self._request_id)
            self._request_id += 1

        ws = self._ws
        if ws is None:
            raise WsNotConnected()

        rpc_request = JsonRpcRequest(request_id, method_name, params)
        await ws.send(rpc_request.to_jsons(encoder=self.opts.encoder))

        rpc_response = await self._wait_for_rpc_response(request_id)
        return rpc_response.unwrap()

    async def subscribe(
        self, channel: str, options: Optional[Any] = None, method_name: str = "subscribe"
    ) -> str:
        """
        Subscribes to an JSONRPC stream. Expects to receive back a subscription ID
        identifying the stream, and notifications from the server with that
        subscription ID attached.

        :param channel: name of channel to subscribe to
        :param options: stream options
        :param method_name: RPC method name for subscribing
        :return: subscription ID
        """
        if options is None:
            options = {}

        result = await self.call(method_name, [channel, options])
        if not isinstance(result, str):
            raise RpcMessageFormatException(
                "subscribe message did not return correct format"
            )

        self._subscription_manager.register(result)
        return result

    async def unsubscribe(self, subscription_id: str, method_name: str = "unsubscribe"):
        """
        Unsubscribes from a JSONRPC stream. All future messages from that stream
        are discarded.

        :param subscription_id: subscription ID to delete
        :param method_name: RPC method name for unsubscribing
        """
        response = await self.call(method_name, [subscription_id])
        if response is not True:
            raise RpcExecutionException(
                "unsubscribe call did not return True or error"
            )

        self._subscription_manager.delete(subscription_id)

    async def next_notification(self) -> SubscriptionNotification:
        """
        Returns the next notification from any subscription ID.

        :return: subscription notification
        """
        task = asyncio.create_task(self._subscription_manager.next_all())
        return await self._wait_for_message(
            task, self.opts.notification_timeout_s
        )

    async def notifications(
        self,
    ) -> AsyncGenerator[SubscriptionNotification, None]:
        """
        Returns an async generator for all notifications on the websocket connection

        :return: async generator for all notifications
        """
        async for notification in self._subscription_manager.iter_all():
            yield notification

    async def next_notification_for_id(self, subscription_id: str) -> Any:
        """
        Returns the next notification for the specified subscription ID

        :param subscription_id: filters for specific notification set
        :return: next notification
        """
        task = asyncio.create_task(
            self._subscription_manager.next_for_id(subscription_id)
        )
        return await self._wait_for_message(
            task, self.opts.notification_timeout_s
        )

    async def notifications_for_id(
        self, subscription_id: str
    ) -> AsyncGenerator[Any, None]:
        """
        Returns an async generator for all notifications for a specific subscription ID
        :param subscription_id: filters for a specific notification set
        :return: async generator for notifications
        """
        async for notification in self._subscription_manager.iter_for_id(
            subscription_id
        ):
            yield notification

    async def close(self):
        """
        Closes websocket connection gracefully.

        :return:
        """
        ws = self._ws
        assert ws is not None

        await ws.close()

    async def _read_loop(self):
        ws = self._ws
        assert ws is not None

        async for message in ws:
            # response type
            try:
                response_message = JsonRpcResponse().from_jsons(
                    message, decoder=self.opts.decoder
                )
            except RpcMessageFormatException as e:
                pass
            else:
                await self._response_queue.put(response_message)
                continue

            # notification type
            try:
                subscription_message = JsonRpcRequest().from_jsons(
                    message, decoder=self.opts.decoder
                )
                params = subscription_message.params
                assert isinstance(params, dict)
                await self._subscription_manager.push(
                    params["subscription"], params["result"]
                )
            except RpcMessageFormatException as e:
                await ws.close(3000, "message did not conform to JSON-RPC spec")

    async def _ensure_ws(self):
        ws = self._ws
        await ws.wait_closed()

    async def _wait_for_rpc_response(self, request_id: str) -> JsonRpcResponse:
        task = asyncio.create_task(self._response_queue.get(request_id))
        return await self._wait_for_message(task, self.opts.request_timeout_s)

    async def _wait_for_message(
        self, message_task: "Future[T]", timeout: Optional[int] = None
    ) -> T:
        status_task = self._status_task
        if status_task is None:
            raise WsNotConnected()

        await asyncio.wait(
            [status_task, message_task],
            return_when=asyncio.FIRST_COMPLETED,
            timeout=timeout,
        )

        if message_task.done():
            return message_task.result()

        if status_task.done():
            raise WsNotConnected()

        message_task.cancel()
        raise WsRpcTimedOut()


class WsException(Exception):
    pass


class WsNotConnected(WsException):
    pass


class WsRpcTimedOut(WsException):
    pass
