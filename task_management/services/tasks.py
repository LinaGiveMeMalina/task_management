from uuid import UUID

from fastapi import HTTPException
from starlette import status

from task_management.errors import TaskNotFoundError
from task_management.repos.tasks import TaskRepo
from task_management.schemas.tasks import CreateTaskSchema, Task, UpdateTaskSchema


class TaskService:

    def __init__(self, task_repo: TaskRepo) -> None:
        self.task_repo = task_repo

    async def create(self, task_data: CreateTaskSchema) -> Task:
        return await self.task_repo.create(task_data=task_data)

    async def delete(self, task_id: UUID) -> None:
        await self.task_repo.delete(task_id=task_id)

    async def get_by_id(self, task_id: UUID) -> Task | None:
        try:
            task = await self.task_repo.get_by_id(task_id=task_id)
            return task
        except TaskNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found.",
            ) from error

    async def get_all(self) -> list[Task]:
        return await self.task_repo.get_all()

    async def update(self, task_id: UUID, task_data: UpdateTaskSchema) -> Task | None:
        try:
            task = await self.task_repo.update(task_id=task_id, task_data=task_data)
            return task
        except TaskNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found.",
            ) from error
