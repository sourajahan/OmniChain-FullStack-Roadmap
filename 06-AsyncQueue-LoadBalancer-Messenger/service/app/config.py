from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_url: str = ""
    queue_name: str = "omnichain:messages"
    dlq_name: str = "omnichain:messages:dlq"
    max_retries: int = 3
    instance_id: str = "api-1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
