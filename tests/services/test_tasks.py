from contextlib import nullcontext

import pytest
from fastapi import HTTPException
from starlette import status

from task_management.services.tasks import TaskService


@pytest.mark.asyncio
async def test__create__can_create_task(task_service: TaskService, make_task_data):
    task_data = make_task_data()
    task = await task_service.create(task_data=task_data)

    assert task
    assert task.title == task_data.title
    assert task.description == task_data.description
    assert task.status == task_data.status


@pytest.mark.asyncio
async def test__get_by_id__can_get_task_by_id(
    task_service: TaskService, make_task_data
):
    task = await task_service.create(task_data=make_task_data())

    returned_task = await task_service.get_by_id(task_id=task.task_id)

    assert returned_task
    assert returned_task.task_id == task.task_id
    assert returned_task.title == task.title
    assert returned_task.description == task.description
    assert returned_task.status == task.status


@pytest.mark.asyncio
async def test__get_by_id__not_found_task(task_service: TaskService, faker):
    task_id = faker.uuid4()
    with pytest.raises(HTTPException) as exc_info:
        await task_service.get_by_id(task_id=task_id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == f"Task with ID {task_id} not found."


@pytest.mark.asyncio
async def test__get_all__can_return_all_tasks(
    task_service: TaskService, make_task_data, faker
):
    tasks_data = [
        make_task_data() for _ in range(faker.pyint(min_value=2, max_value=5))
    ]
    tasks = [await task_service.create(task_data=task_data) for task_data in tasks_data]
    task_ids = {task.task_id for task in tasks}

    returned_tasks = await task_service.get_all()

    assert returned_tasks
    assert len(returned_tasks) == len(tasks)
    for returned_task in returned_tasks:
        assert returned_task.task_id in task_ids


@pytest.mark.asyncio
async def test__get_all__return_empty_list(task_service: TaskService):
    assert await task_service.get_all() == []


@pytest.mark.asyncio
async def test__update__can_update(task_service: TaskService, make_task_data):
    task_for_update = await task_service.create(task_data=make_task_data())
    task_data_for_update = make_task_data()

    updated_task = await task_service.update(
        task_id=task_for_update.task_id,
        task_data=task_data_for_update,
    )

    assert updated_task.task_id == task_for_update.task_id
    assert updated_task.title == task_data_for_update.title
    assert updated_task.description == task_data_for_update.description
    assert updated_task.status == task_data_for_update.status


@pytest.mark.asyncio
async def test__update__cannot_update_if_task_not_found(
    task_service: TaskService, faker, make_task_data
):
    task_id = faker.uuid4()
    with pytest.raises(HTTPException) as exc_info:
        await task_service.update(task_id=task_id, task_data=make_task_data())

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == f"Task with ID {task_id} not found."


@pytest.mark.asyncio
async def test__delete__can_delete_task(task_service: TaskService, make_task_data):
    task_for_delete = await task_service.create(task_data=make_task_data())
    await task_service.delete(task_id=task_for_delete.task_id)

    with pytest.raises(HTTPException) as exc_info:
        await task_service.get_by_id(task_id=task_for_delete.task_id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test__delete_does_not_raise_error_if_task_is_not_found(
    task_service: TaskService, faker
):
    with nullcontext():
        await task_service.delete(task_id=faker.uuid4())
