from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.task import TaskStatus, TaskPriority


class SubTaskCreate(BaseModel):
    title: str
    assignee_id: Optional[int] = None


class SubTaskResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    assignee_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCommentCreate(BaseModel):
    content: str


class TaskCommentResponse(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    deadline: Optional[datetime] = None
    assignee_ids: List[int] = []
    tags: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[datetime] = None
    tags: Optional[str] = None


class TaskAssigneeResponse(BaseModel):
    id: int
    user_id: int
    assigned_at: datetime

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    deadline: Optional[datetime]
    created_by_id: int
    tags: Optional[str]
    created_at: datetime
    subtasks: List[SubTaskResponse] = []
    comments: List[TaskCommentResponse] = []
    assignees: List[TaskAssigneeResponse] = []

    class Config:
        from_attributes = True
