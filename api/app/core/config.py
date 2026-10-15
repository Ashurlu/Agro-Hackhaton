from functools import lru_cache
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def normalize_database_url(url: str) -> str:
    """Accept the URLs hosted Postgres providers hand out (Render, Neon, Supabase).

    They use the `postgres://` / `postgresql://` scheme and libpq's `sslmode`,
    while SQLAlchemy with asyncpg needs `postgresql+asyncpg://` and `ssl`.
    """
    parts = urlsplit(url)
    scheme = parts.scheme
    if scheme in ("postgres", "postgresql"):
        scheme = "postgresql+asyncpg"
    query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        if key == "sslmode":
            key = "ssl"
        if key in ("channel_binding", "options"):
            continue  # libpq-only parameters asyncpg rejects
        query.append((key, value))
    return urlunsplit((scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


class Settings(BaseSettings):
    """Runtime configuration, read from environment variables (see .env.example)."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Aqrar İnvestisiya Portalı API"
    environment: str = "demo"
    api_prefix: str = "/api/v1"

    database_url: str = "postgresql+asyncpg://agro:agro@localhost:5433/agro"

    @field_validator("database_url")
    @classmethod
    def asyncpg_url(cls, value: str) -> str:
        return normalize_database_url(value)

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    cookie_name: str = "portal_session"
    cookie_secure: bool = False

    # Login throttling: after this many failures the account is locked for a while.
    max_failed_logins: int = 5
    lockout_minutes: int = 10

    ektis_mode: str = "mock"
    ektis_base_url: str = "http://ektis-mock:8081/ektis/v1"
    ektis_api_key: str = ""
    ektis_hmac_secret: str = ""

    demo_password: str = ""
    upload_dir: Path = Path("/data/uploads")
    max_upload_mb: int = 10
    seed_dir: Path = Path("/seed")

    # Deadlines are stored in UTC and shown in Baku time.
    display_timezone: str = "Asia/Baku"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
