from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    user_id: str
    description: str
    due_date: Optional[datetime] = None


class TodoCreate(TodoBase):
    pass


class TodoItem(TodoBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
