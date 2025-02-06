from pydantic import BaseModel, Field
from typing import Optional, List
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


class SecondaryMemoryResponse(MemoryBase):
    id: Optional[str]
    user_id: Optional[str]
    text: Optional[str]
    embedding: Optional[list[float]]
    model_id: Optional[str]
    created: Optional[datetime]
    updated: Optional[datetime]

    class Config:
        from_attributes = True


class MemorySearchRequest(BaseModel):
    user_id: Optional[str] = None
    text: str
    model_id: Optional[str] = None
    limit: int = 100
    fields: Optional[str] = None


class MemorySearchResponse(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    text: Optional[str] = None
    model_id: Optional[str] = None
    distance: float = None
