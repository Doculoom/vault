from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChannelCreate(BaseModel):
    user_id: str
    channel_type: str
    channel_id: str


class ChannelItem(BaseModel):
    user_id: str
    channel_type: str
    channel_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
