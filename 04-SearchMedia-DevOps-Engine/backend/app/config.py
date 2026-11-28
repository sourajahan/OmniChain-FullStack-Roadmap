from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 60
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 5
    database_path: str = "searchmedia.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


settings = Settings()
