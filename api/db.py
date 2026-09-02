import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


DEFAULT_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8mb4"

ASYNC_DB_URL = os.getenv(
    "MYSQL_URL",
    DEFAULT_DB_URL
)

# RailwayのMYSQL_URLは mysql:// なので
# SQLAlchemyの非同期MySQL用URLに変換する
if ASYNC_DB_URL.startswith("mysql://"):
    ASYNC_DB_URL = ASYNC_DB_URL.replace(
        "mysql://",
        "mysql+aiomysql://",
        1
    )


async_engine = create_async_engine(
    ASYNC_DB_URL,
    echo=True
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session