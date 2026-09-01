import pytest
import pytest_asyncio

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from api.db import Base, get_db
from api.main import app
from api.models.task import Task, Done


TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


test_engine = create_async_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_test_db():
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.dependency_overrides[get_db] = get_test_db

    yield

    app.dependency_overrides.clear()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_task_crud_and_done():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        # 1. TODOを作成
        response = await client.post(
            "/tasks",
            json={"title": "FastAPIを勉強する"}
        )

        assert response.status_code == 200

        created = response.json()

        assert created["title"] == "FastAPIを勉強する"

        task_id = created["id"]


        # 2. 一覧取得
        response = await client.get("/tasks")

        assert response.status_code == 200

        tasks = response.json()

        assert len(tasks) == 1
        assert tasks[0]["title"] == "FastAPIを勉強する"
        assert tasks[0]["done"] is False


        # 3. タイトル変更
        response = await client.put(
            f"/tasks/{task_id}",
            json={"title": "FastAPIのテストを書く"}
        )

        assert response.status_code == 200
        assert response.json()["title"] == "FastAPIのテストを書く"


        # 4. 完了にする
        response = await client.put(
            f"/tasks/{task_id}/done"
        )

        assert response.status_code == 200


        # 5. doneがtrueになったか確認
        response = await client.get("/tasks")

        tasks = response.json()

        assert tasks[0]["done"] is True


        # 6. 未完了に戻す
        response = await client.delete(
            f"/tasks/{task_id}/done"
        )

        assert response.status_code == 200


        # 7. doneがfalseに戻ったか確認
        response = await client.get("/tasks")

        tasks = response.json()

        assert tasks[0]["done"] is False


        # 8. TODOを削除
        response = await client.delete(
            f"/tasks/{task_id}"
        )

        assert response.status_code == 200


        # 9. 空になったことを確認
        response = await client.get("/tasks")

        assert response.status_code == 200
        assert response.json() == []

