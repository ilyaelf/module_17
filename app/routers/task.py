from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import Task,User
from app.schemas import CreateTask,UpdateTask
from sqlalchemy import insert,select,update,delete
from slugify import slugify

router = APIRouter(prefix='/task',tags=['task'])

@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
        tasks = db.scalars(select(Task)).all()
        return tasks

@router.get('/task_id')
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
        task = db.scalar(select(Task).where(Task.id == task_id))
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        else:
            return task

@router.post('/create')
async def create_task(create_task: CreateTask, user_id: int, db: Annotated[Session,Depends(get_db)]):
    user_exists = db.scalar(select(User).where(User.id == user_id))
    if user_exists is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    else:
        db.execute(insert(Task).values(title=create_task.title,
                                       content=create_task.content,
                                       priority=create_task.priority,
                                       slug=slugify(create_task.title),
                                       user_id=user_exists.id))
        db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Sucsessful"
                }

@router.put('/update')
async def update_task(update_task: UpdateTask, task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
            )
    else:
        db.execute(update(Task).where(Task.id == task_id).values(
                                        title=update_task.title,
                                        content=update_task.content,
                                        priority=update_task.priority,
                                        slug=slugify(update_task.title))
                    )
        db.commit()
        return {
                "status_code": status.HTTP_200_OK,
                "transaction": "task updated sucsessfully"
                 }

@router.delete('/delete')
async def delete_task(task_id: int,db: Annotated[Session,Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    else:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "task deleted sucsessfully"
        }