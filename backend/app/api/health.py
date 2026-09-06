from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.db.models import User

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.get("/health/protected")
def protected_health(
    current_user: User = Depends(get_current_user),
):
    return {
        "status": "authenticated",
        "user": current_user.username,
    }