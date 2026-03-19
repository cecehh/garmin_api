from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    garmin_email: Optional[str] = None
    garmin_password: Optional[str] = None

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
