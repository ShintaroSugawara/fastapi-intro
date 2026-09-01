import asyncio

from api.db import Base, async_engine
from api.models.task import Task, Done


async def migrate():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(migrate())

