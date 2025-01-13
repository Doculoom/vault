from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TodoBase(BaseModel):
    user_id: str
    description: Dict[str, Any]
    due_date: Optional[datetime] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    description: Optional[Dict[str, Any]] = None
    due_date: Optional[datetime] = None


class TodoItem(TodoBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated: Optional[datetime] = None

    class Config:
        orm_mode = True
