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
from db.models.todo import Todo
from db.repository.todo_queries import create_todo ,update_todo , get_todo_by_id
from db.repository.user_queries import get_user_by_id, update_user_by_user
from db.session import get_db
from schemas.todo import TodoCreate, TodoUpdate
from schemas.token import Token

todo_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@todo_router.post("/todo", response_model=TodoCreate)
def create_todo_method(todo: TodoCreate,token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    invalidUserOrId = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User id does not exist",
    )
    invalidToken= HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
    )
    
    try:
      userID = get_user_id_from_token(token)
      print(userID)
    except:
      return invalidToken
    
    try:
      user = get_user_by_id(userID,db=db)
    except:
      return invalidUserOrId
    
    
    result = create_todo(todo,userID,db=db) 
    return result


@todo_router.get("/{todo_id}", response_model=TodoUpdate)
def get_todo_method(todo_id: str,token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    invalidUserOrId = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User id does not exist",
    )
    invalidToken= HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
    )
    
    try:
      userID = get_user_id_from_token(token)
      print(userID)
    except:
      return invalidToken
    
    try:
      user = get_user_by_id(userID,db=db)
    except:
      return invalidUserOrId
    
    
    result = get_todo_by_id(todo_id,db=db)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with this id {id} does not exist",
        )
        
    response_result= TodoUpdate(id=result.id,title=result.title,description=result.description,complete=result.complete) 
    return response_result

@todo_router.patch("/todo", response_model=TodoUpdate)
def update_todo_method(todo: TodoUpdate,token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    invalidUserOrId = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User id does not exist",
    )
    invalidToken= HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
    )
    
    try:
      userID = get_user_id_from_token(token)
    except:
      return invalidToken
    result = update_todo(todo=todo,db=db)    
    
    return result