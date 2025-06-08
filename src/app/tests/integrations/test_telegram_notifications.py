import pytest

from app.config import AppConfig
from app.lib.contrib.telegram import TelegramNotificationClient

pytestmark = pytest.mark.asyncio


async def test_telegram_notification(config: AppConfig):
    if config.telegram.chat_id is None or config.telegram.bot_token is None:
        pytest.skip("TELEGRAM_CHAT_ID is not set")

    telegram = TelegramNotificationClient(bot_token=config.telegram.bot_token)
    res = await telegram.send_notification(chat_id=config.telegram.chat_id, message="hello world")

    assert res.get("status", 500) == 200, res
