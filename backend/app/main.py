from fastapi import FastAPI

app = FastAPI(
    title="SIH26188 Document Screening API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "SIH26188",
        "message": "Document Screening API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }