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

# Enum for task status


class StatusEnum(str, enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"


class TaskEntity(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    content = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.todo)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)

# Pydantic models


class TaskCreate(BaseModel):
    content: str
    status: StatusEnum = StatusEnum.todo
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[StatusEnum] = None
    completed_at: Optional[datetime] = None
    deadline: Optional[datetime] = None


class TaskRead(BaseModel):
    id: UUID
    content: str
    status: StatusEnum
    created_at: datetime
    completed_at: Optional[datetime]
    deadline: Optional[datetime]

    class Config:
        orm_mode = True


Base.metadata.create_all(engine)
