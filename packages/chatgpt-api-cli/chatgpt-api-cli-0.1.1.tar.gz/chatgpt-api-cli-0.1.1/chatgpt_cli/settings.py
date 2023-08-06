from pydantic import BaseSettings

from pathlib import Path


class Settings(BaseSettings):
    openai_api_key: str = None

    class Config:
        env_file = Path.home() / ".chatgpt-cli/.env"
        env_file_encoding = "utf-8"


cli_settings = Settings()
