import os
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.db.schemas import UserCreate, UserResponse, UserLogin

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(
            (User.username == user.username)
            | (User.email == user.email)
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered",
        )

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = (
        db.query(User)
        .filter(User.username == form_data.username)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    if not pwd_context.verify(
        form_data.password,
        db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token_data = {
        "sub": str(db_user.id),
        "username": db_user.username,
        "exp": expire,
    }

    access_token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }