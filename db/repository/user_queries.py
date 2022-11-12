from db.models.user import User
from sqlalchemy.orm import Session
from session import db




def get_user_by_id(id: str):
    user = db.query(User).filter(User.id == id).first()
    return user


def create_user(user: User):
    db.add(user)
    db.commit()
    return user

def update_user(user: User):
    db.update(user)
    db.commit()
    return user