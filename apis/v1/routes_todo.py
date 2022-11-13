from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from apis.utils import OAuth2PasswordBearerWithCookie
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token, get_user_id_from_token
from db.repository.todo_queries import create_todo 
from db.repository.user_queries import get_user_by_id , update_user_by_user

from db.session import get_db
from schemas.todo import TodoCreate, TodoUpdate
from schemas.token import Token

todo_router = APIRouter()


@todo_router.post("/todo", response_model=TodoCreate)
def create_user(self,todo: TodoCreate,token: str = Depends(OAuth2PasswordBearer)):
    invalidUserOrId = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User id does not exist",
    )
    invalidToken= HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
    )
    
    try:
      userID = get_user_id_from_token(self,token)
    except:
      return invalidToken
    
    try:
      user = get_user_by_id(userID)
    except:
      return invalidUserOrId
    
    
    todo = create_todo(todo,userID) 
    return todo


@todo_router.patch("/todo", response_model=TodoUpdate)
def update_user(self,todo: TodoCreate,token: str = Depends(OAuth2PasswordBearer)):
    invalidUserOrId = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User id does not exist",
    )
    invalidToken= HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
    )
    
    try:
      userID = get_user_id_from_token(self,token)
    except:
      return invalidToken
    
    try:
      user = get_user_by_id(userID)
    except:
      return invalidUserOrId
    
    
    todo = update_user_by_user(user) 
    return todo