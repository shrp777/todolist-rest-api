import os
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, func

from pydantic import BaseModel

from datetime import datetime

from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import enum
import os


DB_URL = os.getenv('DATABASE_URL')

engine = create_engine(
    DB_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TaskStatus(str, enum.Enum):
    # Enum pour définir le statut d'un utem Task
    todo = "todo"
    doing = "doing"
    done = "done"


class TaskEntity(Base):
    # Modèle pour définir la table de données tasks
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    content = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)

# Pydantic models


class TaskStatusDTO(BaseModel):
    # Modèle pour la mise à jour du statut d'un item Task
    id: str
    status: TaskStatus = TaskStatus.todo


class TaskCreateDTO(BaseModel):
    # Modèle pour la création d'un item Task
    content: str
    status: TaskStatus = TaskStatus.todo
    deadline: Optional[datetime] = None


class TaskUpdateDTO(BaseModel):
    # Modèle pour la mise à jour d'un item Task
    id: str
    content: Optional[str] = None
    status: Optional[TaskStatus] = None
    completed_at: Optional[datetime] = None
    deadline: Optional[datetime] = None


class TaskReadDTO(BaseModel):
    # Modèle pour la lecture d'un item Task
    id: str
    content: str
    status: TaskStatus
    created_at: datetime
    completed_at: Optional[datetime]
    deadline: Optional[datetime]

    class Config:
        orm_mode = True


Base.metadata.create_all(engine)
