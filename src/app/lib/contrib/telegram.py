import logging

from dataclasses import dataclass
from datetime import UTC, datetime

from httpx import AsyncClient, AsyncHTTPTransport

from .base import BaseNotificationClient


@dataclass
class TelegramNotificationClient(BaseNotificationClient):
    bot_token: str

    _transport = AsyncHTTPTransport(retries=3)

    @property
    def http_client(self):
        return AsyncClient(
            transport=self._transport,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    # todo: outbox pattern
    async def send_notification(
        self,
        chat_id: str,
        message: str,
        *,
        disable_notification: bool = False,
    ):
        url = f"https://api.telegram.org/bot{self.bot_token}" + "/sendMessage"
        meta = f"[{datetime.now(UTC)}] {self.__class__.__name__}"
        telegram_msg = f"\n{message}\n\n{meta}"
        json_data = {
            "chat_id": chat_id,
            "text": telegram_msg,
            "disable_notification": disable_notification,
        }
        r = await self.http_client.post(url, params=json_data)
        logging.debug(f"Sended telegram message: {r.status_code} {r.url}")
        logging.debug(f"Response: {r.json()}")
        return {"status": r.status_code, "description": r.text}
