from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Channel(BaseModel):
    user_id: str
    user_name: Optional[str] = None
    channel_type: Optional[str] = "telegram"
    channel_id: str


class ChannelItem(BaseModel):
    user_id: str
    user_name: str
    channel_type: str
    channel_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
