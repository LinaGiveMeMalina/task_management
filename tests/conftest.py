import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from task_management.settings.settings import settings
from task_management.app import app
from task_management.dependencies import get_task_service
from task_management.enums import TaskStatus
from task_management.models.base import BaseModel
from task_management.repos.tasks import TaskRepo
from task_management.schemas.tasks import CreateTaskSchema
from task_management.services.tasks import TaskService


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(str(settings.test_db.url), echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def cleanup_db(session):
    for table in reversed(BaseModel.metadata.sorted_tables):
        await session.execute(table.delete())
    await session.commit()


@pytest_asyncio.fixture
def task_repo(session):
    return TaskRepo(session)


@pytest_asyncio.fixture
def task_service(task_repo):
    return TaskService(task_repo)


@pytest_asyncio.fixture
async def client(task_service: TaskService):
    app.dependency_overrides[get_task_service] = lambda: task_service
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def make_task_data(faker):
    def inner(
        title: str | None = None,
        description: str | None = None,
        status: TaskStatus | None = None,
    ) -> CreateTaskSchema:
        return CreateTaskSchema(
            title=title or faker.pystr(),
            description=description or faker.pystr(),
            status=status or TaskStatus.CREATED,
        )

    return inner
