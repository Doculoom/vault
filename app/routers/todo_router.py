from fastapi import APIRouter
from typing import List
from datetime import datetime

from app.services.firestore_service import FirestoreService
from app.models.todo_model import TodoCreate, TodoItem

router = APIRouter()
firestore_service = FirestoreService()


@router.post("/todos", response_model=TodoItem)
def create_todo(todo_data: TodoCreate):
    user_id = todo_data.user_id

    doc_data = {
        "description": todo_data.description,
        "due_date": todo_data.due_date.isoformat() if todo_data.due_date else None,
        "created": datetime.utcnow().isoformat()
    }
    todo_id = firestore_service.create_todo(user_id, doc_data)

    return TodoItem(
        id=todo_id,
        user_id=user_id,
        description=doc_data["description"],
        due_date=todo_data.due_date,
        created=datetime.fromisoformat(doc_data["created"])
    )


@router.get("/todos", response_model=List[TodoItem])
def list_todos(user_id: str):
    docs = firestore_service.list_todos(user_id)
    results = []
    for doc in docs:
        results.append(TodoItem(
            id=doc["id"],
            user_id=doc["user_id"],
            description=doc["description"],
            due_date=datetime.fromisoformat(doc["due_date"]) if doc["due_date"] else None,
            created=datetime.fromisoformat(doc["created"])
        ))
    return results
