from db.models.user import User
from sqlalchemy.orm import Session
from db.session import SessionLocal , get_db
from schemas.users import UserCreate



def get_user_by_id(id: str,db:Session):
    user = db.query(User).filter(User.id == id).first()
    return user

def get_user_by_username(username: str,db:Session):
    user = db.query(User).filter(User.username == username).first()
    return user

def create_user(user_create: UserCreate,db:Session):
    user_object = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=user_create.password,
        is_email_confirmed=False
    )
    if (is_username_unique(user_object,db=db)&is_email_unique(user_object,db=db)):
        return False
    db.add(user_object)
    db.commit()
    return user_create

def update_user_by_user(user: User,db:Session):
    db.refresh(user)
    db.commit()
    return user


def is_username_unique(user: User,db:Session):
    if (db.query(User).filter(User.username != user.username).all.size == 0):
        return True
    return False

def is_email_unique(user: User,db:Session):
    if (db.query(User).filter(User.email != user.email).all.size == 0):
        return True
    return False