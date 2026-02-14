from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="MESHCHAT_"
    )
    
    port: int = 2323
    room_name: str = "Chat Room"
    max_users: int = 10
    enable_history: bool = False
    history_size: int = 50
    plain_text: bool = False
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
