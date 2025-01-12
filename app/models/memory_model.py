from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MemoryBase(BaseModel):
    user_id: str
    text: str
    embedding: Optional[list[float]] = None
    model_id: Optional[str] = None


class MemoryCreate(MemoryBase):
    pass


class MemoryUpdate(MemoryBase):
    pass


class SecondaryMemory(MemoryBase):
    id: str
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
