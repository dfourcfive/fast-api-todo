from db.models.user import User
from sqlalchemy.orm import Session
from session import db




def get_user_by_id(id: str):
    user = db.query(User).filter(User.id == id).first()
    return user

def get_user_by_username(username: str):
    user = db.query(User).filter(User.username == username).first()
    return user

def create_user(user: User):
    if (is_username_unique(user)&is_email_unique(user)):
        return False
    db.add(user)
    db.commit()
    return user

def update_user(user: User):
    db.update(user)
    db.commit()
    return user


def is_username_unique(user: User):
    if len(db.query(User).filter(User.username != user.username)) == 0:
        return True
    return False

def is_email_unique(user: User):
    if len(db.query(User).filter(User.email != user.email)) == 0:
        return True
    return False