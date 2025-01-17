import uuid
from typing import Dict, Any

from google.cloud.firestore_v1.base_query import FieldFilter
from app.services.firestore.base import FirestoreBaseService


class FirestoreTodoService(FirestoreBaseService):
    def __init__(self):
        super().__init__()
        self.collection = self.db.collection("todos")

    def create_todo(self, user_id: str, data: Dict[str, Any]) -> str:
        new_id = str(uuid.uuid4())
        data["id"] = new_id
        data["user_id"] = user_id
        doc_ref = self.collection.document(new_id)
        doc_ref.set(data)
        return new_id

    def list_todos(self, user_id: str) -> list:
        query = self.collection.where(filter=FieldFilter("user_id", "==", user_id))
        docs = query.stream()
        return [doc.to_dict() for doc in docs]

    def get_todo(self, user_id: str, todo_id: str) -> dict:
        doc = self.collection.document(todo_id).get()
        if doc.exists:
            data = doc.to_dict()
            if data.get("user_id") == user_id:
                return data
        return {}

    def update_todo(self, user_id: str, todo_id: str, data: dict) -> None:
        doc_ref = self.collection.document(todo_id)
        existing = doc_ref.get().to_dict()
        if existing and existing.get("user_id") == user_id:
            doc_ref.update(data)
        else:
            raise Exception("Todo not found or access denied")
