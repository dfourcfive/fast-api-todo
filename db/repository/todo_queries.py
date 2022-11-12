from db.models.todo import Todo
from db.models.user import User

from sqlalchemy.orm import Session
from session import db
from user_queries import get_user_by_id,update_user

def get_todos_by_userId(id: str):
    result = db.query(Todo).filter(Todo.owner_id == id)
    return result

def get_todo_by_id(id: str):
    result = db.query(Todo).filter(Todo.id == id).first
    return result

def create_todo(todo: Todo,id: str):
    todo = db.add(todo)
    db.commit()
    return todo

def update_user(todo: Todo):
    db.update(todo)
    db.commit()
    return todo