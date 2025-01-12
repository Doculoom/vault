from fastapi import FastAPI
from app.routers import memory_router, todo_router

app = FastAPI(title="Vault Service", version="1.0.0")

app.include_router(memory_router.router, prefix="/api/v1", tags=["memories"])
app.include_router(todo_router.router, prefix="/api/v1", tags=["todos"])


@app.get("/health")
def health_check():
    return {"status": "OK"}
