import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_create_memory():
    payload = {
        "user_id": "test_user",
        "text": "This is a test memory",
        "embedding": None,
        "model_id": "sentence-transformers/all-MiniLM-L6-v2"
    }
    response = client.post("/api/v1/memories", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["text"] == payload["text"]
