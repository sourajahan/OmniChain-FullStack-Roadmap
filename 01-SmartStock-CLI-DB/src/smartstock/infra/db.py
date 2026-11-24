import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    user = os.getenv("DB_USER", "smartstock_app")
    password = os.getenv("DB_PASSWORD", "change_me_local")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "smartstock")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"


class Base(DeclarativeBase):
    pass


engine = create_engine(get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
