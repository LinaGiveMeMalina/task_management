from pydantic_settings import BaseSettings, SettingsConfigDict

from task_management.settings.db import DBSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="_", env_file=".env", extra="ignore"
    )

    db: DBSettings
    test_db: DBSettings


settings = Settings()  # type: ignore[call-arg]
