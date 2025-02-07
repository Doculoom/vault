from datetime import datetime
from typing import Optional, Dict

from google.cloud.firestore_v1.base_query import FieldFilter

from app.services.firestore.base import FirestoreBaseService


class FirestoreChannelService(FirestoreBaseService):
    def __init__(self):
        super().__init__()
        self.collection = self.db.collection("user_channels")

    def get_channel(self, user_id: str, channel_type: str) -> Optional[Dict]:
        doc_ref = (
            self.collection
            .where(filter=FieldFilter("user_id", "==", user_id))
            .where(filter=FieldFilter("channel_type", "==", channel_type))
            .limit(1)
        )
        docs = doc_ref.stream()
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def create_or_update_channel(self, user_id: str, user_name: str, channel_type: str, channel_id: str) -> Dict:
        now_iso = datetime.utcnow().isoformat()
        existing = self.get_channel(user_id, channel_type)

        if existing:
            updated_channel_id = channel_id or existing.get("channel_id")
            updated_channel_type = channel_type or existing.get("channel_type")
            updated_user_name = user_name or existing.get("user_name")
            update_data = {
                "channel_id": updated_channel_id,
                "channel_type": updated_channel_type,
                "user_name": updated_user_name,
                "updated_at": now_iso
            }
            doc_id = existing["id"]
            self.collection.document(doc_id).update(update_data)
            existing.update(update_data)
            return existing
        else:
            data = {
                "user_id": user_id,
                "user_name": user_name,
                "channel_type": channel_type,
                "channel_id": channel_id,
                "created_at": now_iso,
                "updated_at": now_iso,
            }
            doc_ref = self.collection.add(data)
            doc_id = doc_ref[1].id
            data["id"] = doc_id
            return data
