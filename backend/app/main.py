from fastapi import FastAPI

app = FastAPI(
    title="SIH26188 - Fake Identity & Document Screening System",
    version="1.0.0",
)


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