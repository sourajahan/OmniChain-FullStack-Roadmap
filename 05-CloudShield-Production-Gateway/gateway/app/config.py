from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_secret_key: str = "dev-only-change-in-production-32chars"
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if self.app_env.lower() == "production":
            if len(self.api_secret_key) < 32 or "replace-with" in self.api_secret_key or "dev-only" in self.api_secret_key:
                raise ValueError("Production requires a strong API_SECRET_KEY (>= 32 chars, non-default).")
        return self

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


settings = Settings()
