import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from app.main import app
from app.db.base import Base
from app.db.session import get_session
from app.db.uow import UnitOfWork
from app.services.fakedata import FakeDataService


TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres_test:5432/api_test"


engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA IF EXISTS info_api CASCADE"))
        await conn.execute(text("CREATE SCHEMA info_api"))
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        uow = UnitOfWork(session)
        fake_data_service = FakeDataService(uow)

        await fake_data_service.create_full_fake_data(count=20)

    yield

    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA IF EXISTS info_api CASCADE"))

    await engine.dispose()


@pytest.fixture
async def session():
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as test_client:
        yield test_client