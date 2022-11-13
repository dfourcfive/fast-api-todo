from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Optional
import jwt
from jose import JWTError
from core.config import settings
from db.repository.user_queries import get_user_by_username
from fastapi import status
import base64


def create_access_token(self,data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    secret = base64.b64decode(settings.SECRET_KEY) 
    encoded_jwt = jwt.JWT.encode(self,to_encode, jwt.jwk_from_pem(pem_content=secret), alg=settings.ALGORITHM)
    return encoded_jwt

def get_current_user_from_token(
    token: str
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        id: str = payload.get("id")
        print("id extracted is ", id)
        if id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(id=id)
    if user is None:
        raise credentials_exception
    return 


def get_user_id_from_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        id: str = payload.get("id")
        print("id extracted is ", id)
        if id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return id