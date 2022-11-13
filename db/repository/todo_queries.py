from db.models.todo import Todo
from db.models.user import User

from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.user_queries import get_user_by_id
from schemas.todo import TodoCreate
db = get_db

def get_todos_by_userId(id: str):
    result = db.query(Todo).filter(Todo.owner_id == id)
    return result

def get_todo_by_id(id: str):
    result = db.query(Todo).filter(Todo.id == id).first
    return result

def create_todo(todo: TodoCreate,id: str):
    todo_object = Todo(**TodoCreate.dict(todo), owner_id=id)
    todo = db.add(todo)
    db.commit()
    return todo

def update_user(todo: Todo):
    db.update(todo)
    db.commit()
    return todo