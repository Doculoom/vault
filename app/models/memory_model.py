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
    updated: Optional[datetime] = None

    class Config:
        from_attributes = True


class MemorySearchRequest(BaseModel):
    user_id: str
    text: str
    model_id: Optional[str] = None
    limit: int = 5


class MemorySearchResult(BaseModel):
    id: str
    user_id: str
    text: str
    model_id: Optional[str] = None
    distance: float
