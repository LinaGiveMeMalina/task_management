from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from task_management.orm.session import get_db_session
from task_management.repos.tasks import TaskRepo
from task_management.services.tasks import TaskService


def get_task_service(session: AsyncSession = Depends(get_db_session)) -> TaskService:
    return TaskService(TaskRepo(session))
