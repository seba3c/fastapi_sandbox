import pytest
from httpx import AsyncClient, ASGITransport

from app.api.dependencies import get_db_session
from app.core.config import Settings
from app.db.base import Base
from app.db.session import create_async_engine_instance, create_async_session_maker
from app.main import app
from app.repositories.categories import CategoryRepository
from app.schemas.category import CategoryCreate


@pytest.fixture(scope="module")
async def db_engine():
    settings = Settings()
    engine = create_async_engine_instance(settings)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):
    session_maker = create_async_session_maker(db_engine)
    async with db_engine.connect() as connection:
        await connection.begin()
        await connection.begin_nested()
        session = session_maker(bind=connection)
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
