import pytest

from task_management.errors import TaskNotFoundError


@pytest.mark.asyncio
async def test__create__can_create_task(task_repo, make_task_data):
    task_data = make_task_data()
    task = await task_repo.create(task_data=task_data)

    assert task
    assert task.title == task_data.title
    assert task.description == task_data.description
    assert task.status == task_data.status


@pytest.mark.asyncio
async def test__get_by_id__can_get_task_by_id(task_repo, make_task_data):
    task = await task_repo.create(task_data=make_task_data())

    returned_task = await task_repo.get_by_id(task_id=task.task_id)

    assert returned_task
    assert returned_task.task_id == task.task_id
    assert returned_task.title == task.title
    assert returned_task.description == task.description
    assert returned_task.status == task.status


@pytest.mark.asyncio
async def test__get_by_id__raise_error_when_task_not_found(task_repo, faker):
    with pytest.raises(TaskNotFoundError):
        await task_repo.get_by_id(task_id=faker.uuid4())


@pytest.mark.asyncio
async def test__get_all__can_return_all_tasks(task_repo, make_task_data, faker):
    tasks_data = [
        make_task_data() for _ in range(faker.pyint(min_value=2, max_value=5))
    ]
    tasks = [await task_repo.create(task_data=task_data) for task_data in tasks_data]
    task_ids = {task.task_id for task in tasks}

    returned_tasks = await task_repo.get_all()

    assert returned_tasks
    assert len(returned_tasks) == len(tasks)
    for returned_task in returned_tasks:
        assert returned_task.task_id in task_ids


@pytest.mark.asyncio
async def test__get_all__return_empty_list(task_repo, make_task_data):
    returned_tasks = await task_repo.get_all()

    assert returned_tasks == []


@pytest.mark.asyncio
async def test__update__can_update_task(task_repo, make_task_data):
    old_task = await task_repo.create(task_data=make_task_data())
    task_data_for_update = make_task_data()

    updated_task = await task_repo.update(
        task_id=old_task.task_id, task_data=task_data_for_update
    )

    assert updated_task
    assert updated_task.task_id == old_task.task_id
    assert updated_task.title == task_data_for_update.title
    assert updated_task.description == task_data_for_update.description
    assert updated_task.status == task_data_for_update.status


@pytest.mark.asyncio
async def test__update__raise_error_when_task_not_found(task_repo, make_task_data, faker):
    task_data_for_update = make_task_data()

    with pytest.raises(TaskNotFoundError):
        await task_repo.update(task_id=faker.uuid4(), task_data=task_data_for_update)


@pytest.mark.asyncio
async def test_delete_task(task_repo, make_task_data):
    task = await task_repo.create(task_data=make_task_data())
    await task_repo.delete(task_id=task.task_id)

    assert not await task_repo.get_all()
