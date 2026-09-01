from typing import Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: Optional[str] = Field(
        None,
        examples=["クリーニングを取りに行く"]
    )


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    id: int


class Task(TaskBase):
    id: int
    done: bool = Field(
        False,
        description="完了フラグ"
)

