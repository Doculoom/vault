from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.models.channel_model import ChannelItem, Channel
from app.services.firestore.channel_service import FirestoreChannelService

router = APIRouter()
channel_service = FirestoreChannelService()


@router.post("/channels", response_model=ChannelItem)
def create_or_update_channel(channel_data: Channel):
    record = channel_service.create_or_update_channel(
        channel_data.user_id,
        channel_data.user_name,
        channel_data.channel_type,
        channel_data.channel_id
    )

    if not record:
        raise HTTPException(status_code=404, detail="Channel not found after creation/update.")

    return ChannelItem(
        user_id=record["user_id"],
        user_name=record["user_name"],
        channel_type=record["channel_type"],
        channel_id=record["channel_id"],
        created_at=datetime.fromisoformat(record.get("created_at")) if record.get("created_at") else None,
        updated_at=datetime.fromisoformat(record.get("updated_at")) if record.get("updated_at") else None
    )


@router.get("/channels/{user_id}/{channel_type}", response_model=ChannelItem)
def get_channel(user_id: str, channel_type: str):
    record = channel_service.get_channel(user_id, channel_type)
    if not record:
        raise HTTPException(status_code=404, detail="Channel not found")

    return ChannelItem(
        user_id=record["user_id"],
        channel_type=record["channel_type"],
        channel_id=record["channel_id"],
        created_at=datetime.fromisoformat(record["created_at"]) if "created_at" in record else None,
        updated_at=datetime.fromisoformat(record["updated_at"]) if "updated_at" in record else None
    )
