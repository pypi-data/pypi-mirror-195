import asyncio
from typing import Dict, Optional

from jsonrpc.types import JsonRpcResponse


class ResponseQueue:
    """
    Queue for matching RPC requests with responses.
    Usage of this class expects all RPC requests to contain request IDs.

    This class doesn't clean up its memory usage, so if the corresponding RPC
    server doesn't respond to request IDs this queue will continue growing.

    This class does not properly handle multiple requests with the same request_id,
    but you probably shouldn't be doing that anyway.
    """

    def __init__(self):
        self.message_notifiers: Dict[str, asyncio.Event] = {}
        self.message_by_request_id: Dict[str, JsonRpcResponse] = {}

    async def put(self, message: JsonRpcResponse) -> None:
        """
        Upon receiving an RPC response, `put` should be called to signal to the request waiter
        that a response is ready.

        :param message: RPC response
        """
        request_id = message.id
        if request_id is None:
            raise ValueError(
                "Response queue cannot accept RPC messages with no request ID."
            )
        self.message_by_request_id[request_id] = message

        if request_id in self.message_notifiers:
            self.message_notifiers[request_id].set()

    async def get(self, request_id: str) -> Optional[JsonRpcResponse]:
        """
        After dispatching an RPC request, `get` should be called to await its response.

        :param request_id: RPC request id
        :return: RPC response
        """
        if request_id == "":
            raise ValueError("request_id cannot be empty")

        # message has already been answered: return immediately
        if request_id in self.message_by_request_id:
            message = self.message_by_request_id[request_id]
            self._cleanup(request_id)
            return message

        if request_id in self.message_notifiers:
            event = self.message_notifiers[request_id]
        else:
            event = asyncio.Event()
            self.message_notifiers[request_id] = event

        await event.wait()

        if request_id not in self.message_by_request_id:
            return None

        message = self.message_by_request_id[request_id]
        self._cleanup(request_id)
        return message

    def _cleanup(self, request_id: str) -> None:
        self.message_notifiers.pop(request_id, None)
        self.message_by_request_id.pop(request_id, None)
