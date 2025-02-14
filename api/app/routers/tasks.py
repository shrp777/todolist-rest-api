from fastapi import FastAPI, Response, APIRouter, HTTPException, Depends, status, Response
from typing import Union

from sqlalchemy.orm import Session

from typing import List

from ..models.task import TaskEntity, TaskCreateDTO, TaskReadDTO, TaskUpdateDTO, TaskStatusDTO, TaskStatus

from ..db import get_db

from datetime import datetime

from uuid import UUID, uuid4


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.post("/", status_code=201)
def create_task(task: TaskCreateDTO, db: Session = Depends(get_db)):
    task_to_add = TaskEntity(
        id=str(uuid4()),
        content=task.content,
        status=task.status,
        deadline=task.deadline
    )
    db.add(task_to_add)
    db.commit()
    db.refresh(task_to_add)
    return {"result": "success", "code": 201, "detail": "Task created", "task": task_to_add}


@router.get("/", status_code=200)
def read_all_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(TaskEntity).offset(skip).limit(limit).all()
    return {"result": "success", "code": 200, "tasks": tasks}


@router.get("/{task_id}", status_code=200)
def read_one_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"result": "success", "code": 200, "task": task}


@router.put("/{task_id}", status_code=200)
def update_or_create_task(task_id: str, response: Response, task_update: TaskUpdateDTO, db: Session = Depends(get_db)):
    if task_id != task_update.id:
        raise HTTPException(
            status_code=400, detail="Task id in body is not equal to Task id in URI")

    task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()

    # si l'item n'existe pas on le créé
    if task is None:
        task_to_add = TaskEntity(
            id=task_update.id,
            content=task_update.content,
            status=task_update.status,
            deadline=task_update.deadline
        )
        db.add(task_to_add)
        db.commit()
        db.refresh(task_to_add)
        response.status_code = status.HTTP_201_CREATED
        return {"result": "success", "code": 201, "detail": "Task created", "task": task_to_add}

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)

    if task.status == TaskStatus.done:
        task.completed_at = datetime.now()
    else:
        task.completed_at = None

    db.commit()
    db.refresh(task)
    return {"result": "success", "code": 200, "detail": "Task updated", "task": task}


@router.patch("/{task_id}", status_code=200)
def update_task_status(task_id: str, task_update: TaskStatusDTO, db: Session = Depends(get_db)):

    if task_id != task_update.id:
        raise HTTPException(
            status_code=400, detail="Task id in body is not equal to Task id in URI")

    task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = task_update.status

    if task.status == TaskStatus.done:
        task.completed_at = datetime.now()
    else:
        task.completed_at = None

    db.commit()
    db.refresh(task)
    return {"result": "success", "code": 200, "detail": "Task status updated", "task": task}


@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"result": "success", "code": 200, "detail": "Task deleted"}
