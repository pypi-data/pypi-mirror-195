from typing import Dict, NamedTuple, Any, AsyncGenerator

from .async_live_queue import AsyncLiveQueue

default_queue_size = 5000


class SubscriptionNotification(NamedTuple):
    subscription_id: str
    data: Any
    ok: bool


class SubscriptionClosed(Exception):
    pass


class SubscriptionManager:
    """
    Tracks and handles subscription updates as JSON-RPC notifications. Maintains
    an `AsyncLiveQueue` structure to track messages for each subscription type.

    If queue structures are not properly drained old messages will be discarded.
    """

    queue_limit: int
    all_subscription_notifications: AsyncLiveQueue[SubscriptionNotification]
    subscription_notifications_by_id: Dict[
        str, AsyncLiveQueue[SubscriptionNotification]
    ]

    def __init__(self, queue_limit: int = default_queue_size):
        self.queue_limit = queue_limit
        self.all_subscription_notifications = AsyncLiveQueue(self.queue_limit)
        self.subscription_notifications_by_id = {}

    def register(self, subscription_id: str) -> None:
        """
        Registers a queue for a new subscription ID. Ignores duplicate
        subscription IDs.

        :param subscription_id: subscription ID
        """

        if subscription_id in self.subscription_notifications_by_id:
            return

        self.subscription_notifications_by_id[subscription_id] = AsyncLiveQueue(
            self.queue_limit
        )

    def delete(self, subscription_id: str) -> None:
        """
        Delete subscription ID and pushes an error to all queues listening for
        that particular message.

        :param subscription_id: subscription ID to cancel
        """
        queue = self.subscription_notifications_by_id[subscription_id]
        queue.put_nowait(SubscriptionNotification("", None, False))
        del self.subscription_notifications_by_id[subscription_id]

    async def push(self, subscription_id: str, data: Any) -> None:
        """
        Pushes a new subscription notification to the queues.

        Due to asynchronous scheduling it's possible for a message to be received
        before the subscription is registered. These messages will be dropped.
        """
        notification = SubscriptionNotification(subscription_id, data, True)
        await self.all_subscription_notifications.put(notification)
        if notification.subscription_id in self.subscription_notifications_by_id:
            await self.subscription_notifications_by_id[
                notification.subscription_id
            ].put(notification)

    async def next_all(self) -> SubscriptionNotification:
        """
        Consume notifications from any subscription notification queue.

        :return: notification
        """
        return await self.all_subscription_notifications.get()

    async def iter_all(self) -> AsyncGenerator[SubscriptionNotification, None]:
        while True:
            yield await self.all_subscription_notifications.get()

    async def next_for_id(self, subscription_id: str) -> Any:
        """
        Consume notifications from subscription queue with provided id.

        :param subscription_id: subscription queue to consume from
        :return: notification
        """
        notification = await self.subscription_notifications_by_id[
            subscription_id
        ].get()
        if not notification.ok:
            raise SubscriptionClosed()

        return notification.data

    async def iter_for_id(self, subscription_id: str) -> AsyncGenerator[Any, None]:
        queue = self.subscription_notifications_by_id[subscription_id]

        while True:
            notification = await queue.get()
            if not notification.ok:
                raise SubscriptionClosed()

            yield notification.data
