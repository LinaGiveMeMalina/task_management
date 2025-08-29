from uuid import UUID

from sqlalchemy import func, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from task_management.errors import TaskNotFoundError
from task_management.models.tasks import TaskModel
from task_management.schemas.tasks import CreateTaskSchema, Task, UpdateTaskSchema


class TaskRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_data: CreateTaskSchema) -> Task:
        query = (
            insert(TaskModel)
            .values(task_data.model_dump(mode="json"))
            .returning(TaskModel)
        )
        row = await self.session.execute(query)
        task = row.scalar_one()
        await self.session.commit()

        return self.model_to_schema(task)

    async def delete(self, task_id: UUID) -> None:
        query = (
            update(TaskModel)
            .where(TaskModel.task_id == task_id, TaskModel.deleted_at.is_(None))
            .values(deleted_at=func.now())
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_by_id(self, task_id: UUID) -> Task | None:
        query = select(TaskModel).where(
            TaskModel.task_id == task_id, TaskModel.deleted_at.is_(None)
        )
        row = await self.session.execute(query)
        try:
            task = row.scalar_one()
        except NoResultFound as exception:
            raise TaskNotFoundError from exception

        return self.model_to_schema(task)

    async def get_all(self) -> list[Task]:
        query = select(TaskModel).where(TaskModel.deleted_at.is_(None))
        result = await self.session.execute(query)
        tasks = result.scalars().all()

        return [self.model_to_schema(task) for task in tasks]

    async def update(self, task_id: UUID, task_data: UpdateTaskSchema) -> Task | None:
        query = (
            update(TaskModel)
            .where(TaskModel.task_id == task_id, TaskModel.deleted_at.is_(None))
            .values(
                **task_data.model_dump(mode="json", exclude_unset=True),
                updated_at=func.now(),
            )
            .returning(TaskModel)
        )
        row = await self.session.execute(query)
        try:
            task = row.scalar_one()
        except NoResultFound as exception:
            raise TaskNotFoundError from exception

        await self.session.commit()

        return self.model_to_schema(task)

    @staticmethod
    def model_to_schema(task: TaskModel) -> Task:
        return Task.model_validate(task)
