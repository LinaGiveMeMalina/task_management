import pytest


@pytest.mark.asyncio
async def test__create_task(make_task_data, client):
    task_data = make_task_data()
    response = await client.post("/tasks/", json=task_data.model_dump())

    assert response.status_code == 201

    body = response.json()
    assert body["title"] == task_data.title
    assert body["description"] == task_data.description
    assert body["status"] == task_data.status


@pytest.mark.asyncio
async def test__get_task_by_id(make_task_data, client):
    task_data = make_task_data()
    create_resp = await client.post("/tasks/", json=task_data.model_dump())
    task_id = create_resp.json()["task_id"]

    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["task_id"] == task_id
    assert body["title"] == task_data.title


@pytest.mark.asyncio
async def test__get_task_by_id__not_found_task(client, faker):
    response = await client.get(f"/tasks/{faker.uuid4()}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test__get_all_tasks(make_task_data, client):
    for _ in range(3):
        await client.post("/tasks/", json=make_task_data().model_dump())

    response = await client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3


@pytest.mark.asyncio
async def test__update_task(make_task_data, client):
    task_data = make_task_data()
    created_task = await client.post("/tasks/", json=task_data.model_dump())
    task_id = created_task.json()["task_id"]

    task_data_for_update = make_task_data(title="Updated title")
    response = await client.patch(
        f"/tasks/{task_id}", json=task_data_for_update.model_dump(exclude_unset=True)
    )

    assert response.status_code == 200
    body = response.json()
    assert body["task_id"] == task_id
    assert body["title"] == "Updated title"


@pytest.mark.asyncio
async def test__update_task__not_found_task(client, make_task_data, faker):
    task_data_for_update = make_task_data()
    response = await client.patch(
        f"/tasks/{faker.uuid4()}", json=task_data_for_update.model_dump(exclude_unset=True)
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test__delete_task(make_task_data, client):
    task_data = make_task_data()
    created_task = await client.post("/tasks/", json=task_data.model_dump())
    task_id = created_task.json()["task_id"]

    response = await client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
