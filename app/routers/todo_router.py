from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime


from app.models.todo_model import TodoCreate, TodoUpdate, TodoItem
from app.services.firestore.todo_service import FirestoreTodoService

router = APIRouter()
firestore_service = FirestoreTodoService()


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
        description=todo_data.description,
        due_date=todo_data.due_date,
        created_at=datetime.fromisoformat(doc_data["created"])
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


@router.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: str, update_data: TodoUpdate, user_id: str):
    existing = firestore_service.get_todo(user_id, todo_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Todo not found or access denied")

    updated_description = update_data.description if update_data.description is not None else existing["description"]
    updated_due_date = update_data.due_date if update_data.due_date is not None else existing.get("due_date")

    updated_data = {
        "description": updated_description,
        "due_date": updated_due_date.isoformat() if updated_due_date else None,
        "updated": datetime.utcnow().isoformat()
    }

    try:
        firestore_service.update_todo(user_id, todo_id, updated_data)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

    return TodoItem(
        id=todo_id,
        user_id=user_id,
        description=updated_description,
        due_date=updated_due_date,
        created=datetime.fromisoformat(existing["created"])
    )
