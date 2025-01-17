from typing import List

from fastapi import APIRouter, HTTPException
from datetime import datetime
from google.cloud.firestore_v1.vector import Vector

from app.core.config import settings

from app.services.embeddings_service import EmbeddingsService
from app.models.memory_model import MemoryCreate, MemoryUpdate, SecondaryMemory, MemorySearchResult, MemorySearchRequest
from app.services.firestore.memory_service import FirestoreMemoryService

router = APIRouter()
firestore_service = FirestoreMemoryService()
embeddings_service = EmbeddingsService()


@router.post("/memories", response_model=SecondaryMemory)
def create_memory(memory_data: MemoryCreate):
    user_id = memory_data.user_id

    if memory_data.embedding is None:
        generated_embedding = embeddings_service.generate_embedding(
            text=memory_data.text,
            model_id=memory_data.model_id or settings.EMBEDDING_MODEL_ID
        )
        memory_data.embedding = generated_embedding

    doc_data = {
        "text": memory_data.text,
        "embedding": Vector(memory_data.embedding),
        "model_id": memory_data.model_id or settings.EMBEDDING_MODEL_ID,
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


@router.get("/memories", response_model=List[SecondaryMemory])
def list_memories(user_id: str):
    memories = firestore_service.list_memories(user_id)
    results = []
    for mem in memories:
        results.append(SecondaryMemory(
            id=mem.get("id"),
            user_id=mem.get("user_id"),
            text=mem.get("text"),
            embedding=mem.get("embedding"),
            model_id=mem.get("model_id"),
            created=datetime.fromisoformat(mem["created"]) if mem.get("created") else None,
            updated=datetime.fromisoformat(mem["updated"]) if mem.get("updated") else None
        ))
    return results


@router.get("/memories/{memory_id}", response_model=SecondaryMemory)
def get_memory(memory_id: str, user_id: str):
    memory = firestore_service.get_memory(user_id, memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found or access denied")

    return SecondaryMemory(
        id=memory.get("id"),
        user_id=memory.get("user_id"),
        text=memory.get("text"),
        embedding=memory.get("embedding"),
        model_id=memory.get("model_id"),
        created=datetime.fromisoformat(memory["created"]) if memory.get("created") else None,
        updated=datetime.fromisoformat(memory["updated"]) if memory.get("updated") else None
    )


@router.post("/memories/search", response_model=List[MemorySearchResult])
def search_memories(request: MemorySearchRequest):
    user_id = request.user_id
    embedding = embeddings_service.generate_embedding(
        text=request.text,
        model_id=request.model_id or settings.EMBEDDING_MODEL_ID
    )

    search_results = firestore_service.search_memories(
        user_id=user_id,
        query_embedding=embedding,
        limit=request.limit
    )

    return search_results

