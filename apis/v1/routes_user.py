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
from schemas.users import ShowUser, UserCreate

user_router = APIRouter()


@user_router.post("/register", response_model=ShowUser)
def create_user_route_method(user: UserCreate,db: Session = Depends(get_db)):
    try:
      updated_user = user
      hashed_password = Hasher.get_password_hash(updated_user.password)
      updated_user.password=hashed_password
      print(updated_user.password)
      result = create_user(updated_user,db=db)
      if(result == False):
            raise HTTPException(status_code=404, detail="username or email is not unique")
      print('here no errors so far')
      response=ShowUser(username=result.username,email=result.email,jwt="")
      return response
    except Exception as e:
      print('An exception occurred'+str(e))
      raise HTTPException(status_code=404, detail="an error occured")


@user_router.post("/token", response_model=Token)
def login_for_access_token(
    self,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        self,
        data={"id": user.id}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}



def authenticate_user(username: str, password: str,db: Session = Depends(get_db)):
    user = get_user_by_username(username=username,db=db)

    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user