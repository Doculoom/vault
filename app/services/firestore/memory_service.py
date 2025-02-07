import uuid
from typing import Dict, Any, List, Optional

from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_query import FieldFilter

from app.services.firestore.base import FirestoreBaseService


class FirestoreMemoryService(FirestoreBaseService):
    def __init__(self):
        super().__init__()
        self.collection = self.db.collection("memories")

    def create_memory(self, user_id: str, data: Dict[str, Any]) -> str:
        new_id = str(uuid.uuid4())
        data["id"] = new_id
        data["user_id"] = user_id
        doc_ref = self.collection.document(new_id)
        doc_ref.set(data)
        return new_id

    def update_memory(self, user_id: str, memory_id: str, data: Dict[str, Any]) -> None:
        doc_ref = self.collection.document(memory_id)
        existing = doc_ref.get().to_dict()
        if existing and existing.get("user_id") == user_id:
            doc_ref.update(data)
        else:
            raise Exception("Memory not found or access denied")

    def get_memory(self, user_id: str, memory_id: str) -> Dict[str, Any]:
        doc = self.collection.document(memory_id).get()
        if doc.exists:
            data = doc.to_dict()
            if data.get("user_id") == user_id:
                return data
        return {}

    def list_memories(self, user_id: str, fields: List[str]) -> List[Dict[str, Any]]:
        query = self.collection

        if fields:
            query = self.collection.select(fields)

        if user_id:
            query = query.where(filter=FieldFilter("user_id", "==", user_id))

        docs = query.stream()
        return [doc.to_dict() for doc in docs]

    def search_memories(
            self,
            user_id: Optional[str],
            fields: List[str],
            query_embedding: List[float],
            distance_measure: DistanceMeasure = DistanceMeasure.COSINE,
            limit: int = 5,
    ) -> List[Dict[str, Any]]:
        query = self.collection

        if user_id:
            query = query.where(filter=FieldFilter("user_id", "==", user_id))

        if fields:
            query = self.collection.select(fields)

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
            print(doc_data)
            doc_data["distance"] = doc.get("vector_distance")
            results.append(doc_data)

        return results
