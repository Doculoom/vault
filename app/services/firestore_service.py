from google.cloud import firestore
from typing import Dict, Any, List
import uuid

from app.core.config import settings

from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_query import FieldFilter


class FirestoreService:
    def __init__(self):
        self.client = firestore.Client(
            project=settings.GCP_PROJECT_ID,
            database=settings.DB_NAME
        )
        self.memory_collection = self.client.collection("memories")
        self.todo_collection = self.client.collection("todos")

    def create_memory(self, user_id: str, data: Dict[str, Any]) -> str:
        new_id = str(uuid.uuid4())
        data["id"] = new_id
        data["user_id"] = user_id
        doc_ref = self.memory_collection.document(new_id)
        doc_ref.set(data)
        return new_id

    def update_memory(self, user_id: str, memory_id: str, data: Dict[str, Any]) -> None:
        doc_ref = self.memory_collection.document(memory_id)
        existing = doc_ref.get().to_dict()
        if existing and existing.get("user_id") == user_id:
            doc_ref.update(data)
        else:
            raise Exception("Memory not found or access denied")

    def get_memory(self, user_id: str, memory_id: str) -> Dict[str, Any]:
        doc = self.memory_collection.document(memory_id).get()
        if doc.exists:
            data = doc.to_dict()
            if data.get("user_id") == user_id:
                return data
        return {}

    def list_memories(self, user_id: str) -> list:
        query = self.memory_collection.where(filter=FieldFilter("user_id", "==", user_id))
        docs = query.stream()
        return [doc.to_dict() for doc in docs]

    def create_todo(self, user_id: str, data: Dict[str, Any]) -> str:
        new_id = str(uuid.uuid4())
        data["id"] = new_id
        data["user_id"] = user_id
        doc_ref = self.todo_collection.document(new_id)
        doc_ref.set(data)
        return new_id

    def list_todos(self, user_id: str) -> list:
        query = self.todo_collection.where(filter=FieldFilter("user_id", "==", user_id))
        docs = query.stream()
        return [doc.to_dict() for doc in docs]

    def get_todo(self, user_id: str, todo_id: str) -> dict:
        doc = self.todo_collection.document(todo_id).get()
        if doc.exists:
            data = doc.to_dict()
            if data.get("user_id") == user_id:
                return data
        return {}

    def update_todo(self, user_id: str, todo_id: str, data: dict) -> None:
        doc_ref = self.todo_collection.document(todo_id)
        existing = doc_ref.get().to_dict()
        if existing and existing.get("user_id") == user_id:
            doc_ref.update(data)
        else:
            raise Exception("Todo not found or access denied")

    def search_memories(
            self,
            user_id: str,
            query_embedding: List[float],
            distance_measure: DistanceMeasure = DistanceMeasure.COSINE,
            limit: int = 5
    ) -> List[Dict[str, Any]]:
        query = self.memory_collection.where(filter=FieldFilter("user_id", "==", user_id))
        vector_query = query.find_nearest(
            vector_field="embedding",
            query_vector=Vector(query_embedding),
            distance_measure=distance_measure,
            limit=limit,
            distance_result_field="vector_distance",
        )

        docs = vector_query.stream()
        results = []

        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["distance"] = doc.get("vector_distance")
            results.append(doc_data)

        return results
