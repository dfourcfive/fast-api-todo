from fastapi import APIRouter
from v1 import routes_todo,routes_user

api_router = APIRouter()

api_router.include_router(routes_todo.router, prefix="/todos")
api_router.include_router(routes_user.router, prefix="/users")
