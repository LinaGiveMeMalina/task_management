from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict, Field

from task_management.enums import TaskStatus
from task_management.schemas.base_schema import BaseSchema


class BaseTask(BaseSchema):
    title: str = Field(max_length=32)
    description: str | None = Field(default=None, max_length=255)
    status: TaskStatus = Field(default=TaskStatus.CREATED)

    model_config = ConfigDict(use_enum_values=True, from_attributes=True)


class Task(BaseTask):
    task_id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateTaskSchema(BaseTask):
    pass


class UpdateTaskSchema(BaseSchema):
    title: str | None = Field(default=None, max_length=32)
    description: str | None = Field(default=None, max_length=255)
    status: TaskStatus | None = None

    model_config = ConfigDict(use_enum_values=True)
