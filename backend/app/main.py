from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.db.database import engine
from app.db.models import Base
from app.api.health import router as health_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIH26188 - Fake Identity & Document Screening System",
    version="1.0.0",
)
app.include_router(auth_router)
app.include_router(health_router)
@app.get("/")
def root():
    return {
        "message": "SIH26188 API is running",
        "status": "success",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }