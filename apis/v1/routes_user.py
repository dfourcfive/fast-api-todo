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
from db.repository.user_queries import get_user_by_username , get_user_by_id , create_user
from db.session import get_db
from schemas.token import Token
from schemas.users import ShowUser, UserCreate , UserLogin

user_router = APIRouter()


@user_router.post("/register", response_model=ShowUser)
def create_user_route_method(user: UserCreate,db: Session = Depends(get_db)):
    try:
      updated_user = user
      hashed_password = Hasher.get_password_hash(updated_user.password)
      updated_user.password=hashed_password
      result = create_user(updated_user,db=db)
      print(result)
      if(result == False):
            raise HTTPException(status_code=404, detail="username or email is not unique")
      response=ShowUser(username=result.username,email=result.email,jwt="")
      print(response);
      return response
    except Exception as e:
      print('An exception occurred'+str(e))
      raise HTTPException(status_code=404, detail=(str(e)))


@user_router.post("/token", response_model=Token)
def login_for_access_token(
    user: UserLogin,
    db: Session = Depends(get_db)):
    result = authenticate_user(user.username, user.password,db=db)
    print(result)
    if(result == False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"id": result.id}, expires_delta=access_token_expires
    )
    responseResult = Token(access_token=access_token,token_type="bearer")
    return responseResult



def authenticate_user(username: str, password: str,db: Session = Depends(get_db)):
    user = get_user_by_username(username=username,db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user