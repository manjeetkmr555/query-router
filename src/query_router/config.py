import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: SecretStr
    router_model: str = "openai:gpt-4o-mini"


def load_settings() -> Settings:
    settings = Settings()
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key.get_secret_value()
    return settings
