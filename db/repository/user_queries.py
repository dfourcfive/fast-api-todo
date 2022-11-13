from db.models.user import User
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.users import UserCreate



db = get_db
def get_user_by_id(id: str):
    user = db.query(User).filter(User.id == id).first()
    return user

def get_user_by_username(username: str):
    user = db.query(User).filter(User.username == username).first()
    return user

def create_user(user_create: UserCreate):
    user_object = User(**user_create.dict())
    if (is_username_unique(user_object)&is_email_unique(user_object)):
        return False
    db.add(user_object)
    db.commit()
    return user_create

def update_user_by_user(user: User):
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