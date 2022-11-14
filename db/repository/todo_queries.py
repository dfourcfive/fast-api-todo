from db.models.todo import Todo
from db.models.user import User

from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.user_queries import get_user_by_id
from schemas.todo import TodoCreate , TodoUpdate
from sqlalchemy import update

def get_todos_by_userId(id: str,db:Session):
    result = db.query(Todo).filter(Todo.owner_id == id)
    return result

def get_todo_by_id(id: str,db:Session):
    result = db.query(Todo).filter(Todo.id == id).first
    return result

def create_todo(todo: TodoCreate,id: str,db:Session):
    todo_object = Todo(title=todo.title,description=todo.description,complete=False, owner_id=id)
    db.add(todo_object)
    db.commit()
    return todo

def update_todo(todo: TodoUpdate,db:Session):
    todo_object = Todo(**TodoUpdate.dict(todo))
    db.execute(update(Todo).where(Todo.id==todo.id).values(title=todo.title,description=todo.description,complete=todo.complete))
    db.commit()
    return todo