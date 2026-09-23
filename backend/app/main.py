print("JAI SHRIRAM")

from fastapi import FastAPI

from app.core.config import settings
from app.api.routes.repositories import router as repository_router
from app.api.routes.datasets import router as dataset_router

app = FastAPI(
    title=settings.app_name,
    description="Dataset version control platform",
    version="0.1.0",
)


app.include_router(repository_router)
app.include_router(dataset_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "chronix",
        "environment": settings.app_env,
    }