from app.core.config import normalize_database_url

NEON = "postgresql://u:p@ep-x.neon.tech/agro?sslmode=require&channel_binding=require"


def test_hosted_postgres_urls_become_asyncpg_urls():
    render = normalize_database_url("postgres://u:p@host:5432/agro")
    assert render == "postgresql+asyncpg://u:p@host:5432/agro"
    neon = normalize_database_url(NEON)
    assert neon == "postgresql+asyncpg://u:p@ep-x.neon.tech/agro?ssl=require"


def test_asyncpg_urls_are_left_alone():
    url = "postgresql+asyncpg://agro:agro@db:5432/agro"
    assert normalize_database_url(url) == url
