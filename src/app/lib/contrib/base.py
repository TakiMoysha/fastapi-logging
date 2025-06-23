from typing import Protocol, runtime_checkable


# =================================================


@runtime_checkable
class BaseNotificationClient(Protocol):
    async def send_notification(
        self,
        chat_id: str,
        message: str,
        *,
        disable_notification: bool = False,
    ) -> dict: ...


