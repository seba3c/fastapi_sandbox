import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.dependencies import get_db_session
from app.core.config import Settings
from app.db.base import Base
from app.main import app
from app.repositories.categories import CategoryRepository
from app.schemas.category import CategoryCreate

settings = Settings()


@pytest.fixture(scope="module")
async def db_engine():
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):
    async with db_engine.connect() as connection:
        await connection.begin()
        await connection.begin_nested()
        session_maker = async_sessionmaker(bind=connection, expire_on_commit=False)
        session = session_maker()
        yield session
        await session.close()
        await connection.rollback()


@pytest.fixture
async def repository(db_session):
    return CategoryRepository(db_session)


@pytest.fixture
async def category_factory(repository):
    async def _make(name: str = "Test Category"):
        return await repository.create(CategoryCreate(name=name))

    return _make


@pytest.fixture
async def client(db_session):
    app.dependency_overrides[get_db_session] = lambda: db_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
