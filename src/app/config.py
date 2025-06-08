from dataclasses import dataclass, field
from functools import lru_cache
import os

from app.lib.utils.upcast_env import get_upcast_env


@dataclass
class ServerConfig:
    title: str = "event-box"
    debug: bool = field(default_factory=lambda: get_upcast_env("SERVER_DEBUG", False))
    secret_key: str = field(default_factory=lambda: get_upcast_env("SERVER_SECRET_KEY", "_dont_expose_me_"), repr=False, hash=False)  # fmt: skip
    ws_heartbeat_timeout: int = field(default_factory=lambda: get_upcast_env("SERVER_WS_HEARTBEAT_TIMEOUT", 10))  # fmt: skip


@dataclass
class MongoConfig:
    connection_url: str = field(
        default_factory=lambda: get_upcast_env("DB_CONNECTION_URL", "mongodb://localhost:27017/")
    )
    db_server: str = field(default_factory=lambda: get_upcast_env("DB_SERVER", "server"))
    collection_server: str = field(default_factory=lambda: get_upcast_env("DB_COLLECTION", "server"))


@dataclass
class KafkaConfig:
    bootstrap_servers: str = field(default_factory=lambda: get_upcast_env("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092"))

    new_news_received_topic: str = "news.new"

    new_channel_event_topic: str = "channels.new"
    channel_deleted_topic: str = "channels.deleted"

    new_listener_added_topic: str = "channel.listeners-added"
    new_listener_removed_topic: str = "channel.listeners-removed"


@dataclass
class LoggingConfig:
    app_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_APP_LEVEL", "INFO"))

    uvicorn_access_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_UVICORN_ACCESS_LEVEL", "INFO"))
    uvicorn_error_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_UVICORN_ERROR_LEVEL", "ERROR"))

    saq_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_SAQ_LEVEL", "INFO"))

    sqlalchemy_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_SQLALCHEMY_LEVEL", "WARN"))
    motor_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_MOTOR_LEVEL", "WARN"))

    not_interesting: str = field(default_factory=lambda: get_upcast_env("LOGGING_NOT_INTERESTING_LEVEL", "WARN"))


@dataclass
class TelegramConfig:
    bot_token: str | None = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", None), repr=False, hash=False)
    chat_id: str | None = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_CHAT", None), repr=False, hash=False)


@dataclass
class AppConfig:
    server: ServerConfig = field(default_factory=ServerConfig)
    mongo: MongoConfig = field(default_factory=MongoConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)


@lru_cache(0)
def get_config():
    return AppConfig()
