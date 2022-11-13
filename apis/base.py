from fastapi import APIRouter
from apis.v1.routes_todo import todo_router
from apis.v1.routes_user import user_router

api_router = APIRouter()

api_router.include_router(todo_router, prefix="/todos")
api_router.include_router(user_router, prefix="/users")
