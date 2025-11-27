from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.task import Task, TaskAssignee, TaskComment, SubTask
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskCommentCreate, SubTaskCreate

router = APIRouter()


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        deadline=task_data.deadline,
        created_by_id=current_user.id,
        tags=task_data.tags
    )
    db.add(new_task)
    await db.flush()
    
    for assignee_id in task_data.assignee_ids:
        assignee = TaskAssignee(task_id=new_task.id, user_id=assignee_id)
        db.add(assignee)
    
    await db.commit()
    
    # Загружаем задачу со всеми связанными данными
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.subtasks), selectinload(Task.comments), selectinload(Task.assignees))
        .where(Task.id == new_task.id)
    )
    task = result.scalar_one()
    
    # Отправляем уведомления назначенным пользователям
    if task_data.assignee_ids:
        from app.websocket.manager import manager
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"📋 Sending task notifications to {len(task_data.assignee_ids)} assignees")
        for assignee_id in task_data.assignee_ids:
            logger.info(f"📋 Sending notification to user {assignee_id} for task {new_task.id}")
            await manager.send_task_notification(
                user_id=assignee_id,
                task_id=new_task.id,
                task_title=new_task.title,
                assigned_by=current_user.id
            )
    
    return task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.subtasks), selectinload(Task.comments), selectinload(Task.assignees))
        .offset(skip)
        .limit(limit)
    )
    tasks = result.scalars().all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.subtasks), selectinload(Task.comments), selectinload(Task.assignees))
        .where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.assignees))
        .where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Сохраняем старых assignees для сравнения
    old_assignee_ids = {a.user_id for a in task.assignees}
    
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)
    
    await db.commit()
    
    # Загружаем задачу со всеми связанными данными
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.subtasks), selectinload(Task.comments), selectinload(Task.assignees))
        .where(Task.id == task_id)
    )
    task = result.scalar_one()
    
    # Отправляем уведомления новым assignees
    new_assignee_ids = {a.user_id for a in task.assignees}
    added_assignees = new_assignee_ids - old_assignee_ids
    
    if added_assignees:
        from app.websocket.manager import manager
        for assignee_id in added_assignees:
            await manager.send_task_notification(
                user_id=assignee_id,
                task_id=task.id,
                task_title=task.title,
                assigned_by=current_user.id
            )
    
    return task


@router.post("/{task_id}/comments")
async def add_comment(
    task_id: int,
    comment_data: TaskCommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_comment = TaskComment(
        task_id=task_id,
        user_id=current_user.id,
        content=comment_data.content
    )
    db.add(new_comment)
    await db.commit()
    
    return {"message": "Comment added"}


@router.post("/{task_id}/subtasks")
async def add_subtask(
    task_id: int,
    subtask_data: SubTaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_subtask = SubTask(
        task_id=task_id,
        title=subtask_data.title,
        assignee_id=subtask_data.assignee_id
    )
    db.add(new_subtask)
    await db.commit()
    
    return {"message": "Subtask added"}
