from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.services.firestore_service import FirestoreService
from app.services.embeddings_service import EmbeddingsService
from app.models.memory_model import MemoryCreate, MemoryUpdate, SecondaryMemory

router = APIRouter()
firestore_service = FirestoreService()
embeddings_service = EmbeddingsService()


@router.post("/memories", response_model=SecondaryMemory)
def create_memory(memory_data: MemoryCreate):
    user_id = memory_data.user_id

    if memory_data.embedding is None:
        generated_embedding = embeddings_service.generate_embedding(
            text=memory_data.text,
            model_id=memory_data.model_id
        )
        memory_data.embedding = generated_embedding

    doc_data = {
        "text": memory_data.text,
        "embedding": memory_data.embedding,
        "model_id": memory_data.model_id,
        "created": datetime.utcnow().isoformat()
    }

    memory_id = firestore_service.create_memory(user_id, doc_data)
    return SecondaryMemory(
        id=memory_id,
        user_id=user_id,
        text=doc_data["text"],
        embedding=doc_data["embedding"],
        model_id=doc_data["model_id"],
        created=datetime.fromisoformat(doc_data["created"])
    )


@router.put("/memories/{memory_id}", response_model=SecondaryMemory)
def update_memory(memory_id: str, update_data: MemoryUpdate, user_id: str):
    existing = firestore_service.get_memory(user_id, memory_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Memory not found or access denied")

    updated_text = update_data.text if update_data.text else existing["text"]
    updated_embedding = update_data.embedding or existing["embedding"]
    updated_model_id = update_data.model_id or existing.get("model_id")

    if update_data.text and update_data.embedding is None:
        updated_embedding = embeddings_service.generate_embedding(
            text=update_data.text,
            model_id=updated_model_id
        )

    updated_data = {
        "text": updated_text,
        "embedding": updated_embedding,
        "model_id": updated_model_id,
        "created": existing.get("created", datetime.utcnow().isoformat()),
        "updated": datetime.utcnow().isoformat()
    }

    try:
        firestore_service.update_memory(user_id, memory_id, updated_data)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

    return SecondaryMemory(
        id=memory_id,
        user_id=user_id,
        text=updated_data["text"],
        embedding=updated_data["embedding"],
        model_id=updated_data["model_id"],
        created=datetime.fromisoformat(updated_data["created"]),
        updated=datetime.fromisoformat(updated_data["updated"])
    )
