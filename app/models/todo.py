from sqlalchemy import Boolean, Column, Integer, String
from pydantic import BaseModel
from ..database import Base


# SQLAlchemy Model
class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)


# Pydantic Models
class TodoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True