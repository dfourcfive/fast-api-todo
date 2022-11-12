from datetime import timedelta

import jwt
from jose import JWTError
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from apis.utils import OAuth2PasswordBearerWithCookie
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.repository.user_queries import get_user_by_username , get_user_by_id
from db.session import get_db
from schemas.token import Token
from schemas.users import ShowUser, UserCreate

router = APIRouter()


@router.post("/register", response_model=ShowUser)
def create_user(user: UserCreate):
    user = create_user(user=user)
    return user



@router.post("/token", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}



def authenticate_user(username: str, password: str):
    user = get_user_by_username(username=username)

    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user