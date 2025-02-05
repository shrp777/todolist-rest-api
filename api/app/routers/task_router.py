from fastapi import FastAPI, Response, APIRouter, HTTPException, Depends
from typing import Union

from sqlalchemy.orm import Session

from typing import List

from ..models.task import TaskEntity, TaskCreate, TaskRead, TaskUpdate

from ..db import get_db

from datetime import datetime

from uuid import UUID, uuid4


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

# CRUD Endpoints


@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = TaskEntity(
        id=str(uuid4()),
        content=task.content,
        status=task.status,
        deadline=task.deadline
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskRead])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(TaskEntity).offset(skip).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", response_model=TaskRead)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return task
