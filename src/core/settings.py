import os
from functools import cache
from typing import Literal

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict
from yarl import URL

ENV_FILE_PATH = (
    {
        "local": ".env",
        "ci": ".env.ci",
        "test": ".env.test",
    }
).get(os.getenv("ENV", "local"), ".env")


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="allow",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return super().settings_customise_sources(
            settings_cls,
            init_settings,
            dotenv_settings,
            env_settings,
            file_secret_settings,
        )

    app_title: str = "FastAPI Template Project"
    app_name: str = "fastapi_template"
    env: Literal["local", "test", "ci", "dev", "prod"] = "prod"
    root_path: str = ""

    debug: bool = True

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = ""
    postgres_db: str = ""
    postgres_echo: bool = False

    sentry_dsn: str | None = None

    prometheus_metrics_key: str = "secret"

    @property
    def postgres_url(self) -> str:
        return str(
            URL.build(
                scheme="postgresql+asyncpg",
                host=self.postgres_host,
                port=self.postgres_port,
                user=self.postgres_user,
                password=self.postgres_password,
                path=f"/{self.postgres_db}",
            )
        )


@cache
def get_settings() -> Settings:
    return Settings()
