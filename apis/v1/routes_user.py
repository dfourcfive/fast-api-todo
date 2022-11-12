from db.repository.user_queries import create_new_user
from fastapi import APIRouter
from schemas.users import ShowUser
from schemas.users import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=ShowUser)
def create_user(user: UserCreate):
    user = create_user(user=user)
    return user
