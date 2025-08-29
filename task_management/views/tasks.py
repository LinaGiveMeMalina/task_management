from uuid import UUID

from fastapi import APIRouter, Depends

from task_management.dependencies import get_task_service
from task_management.schemas.tasks import (CreateTaskSchema, Task,
                                           UpdateTaskSchema)
from task_management.services.tasks import TaskService

router = APIRouter(prefix="/tasks", tags=["Менеджер задач"])


@router.post("/", response_model=Task, status_code=201, summary="Создать задачу")
async def create_task(
    task_data: CreateTaskSchema,
    service: TaskService = Depends(get_task_service),
) -> Task:
    return await service.create(task_data=task_data)


@router.delete("/{task_id}", summary="Удалить задачу")
async def delete_task(
    task_id: UUID, service: TaskService = Depends(get_task_service)
) -> None:
    await service.delete(task_id=task_id)


@router.get("/{task_id}", response_model=Task, summary="Получить задачу по ID")
async def get_task_by_id(
    task_id: UUID, service: TaskService = Depends(get_task_service)
) -> Task:
    return await service.get_by_id(task_id=task_id)


@router.get("/", response_model=list[Task], summary="Получить список всех задач")
async def get_all_tasks(service: TaskService = Depends(get_task_service)) -> list[Task]:
    return await service.get_all()


@router.patch("/{task_id}", response_model=Task, summary="Обновить задачу")
async def update_task(
    task_id: UUID,
    task_data: UpdateTaskSchema,
    service: TaskService = Depends(get_task_service),
) -> Task:
    return await service.update(task_id=task_id, task_data=task_data)
