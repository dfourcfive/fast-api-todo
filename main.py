from datetime import timedelta
import datetime
from typing import Union
from fastapi import FastAPI
import jwt
from core.config import settings
from db.session import engine   #new
from db.base import Base

JWT_SECRET = "secret_key" # IRL we should NEVER hardcode the secret: it should be an evironment variable!!!
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


def create_tables():           #new
	Base.metadata.create_all(bind=engine)

def start_application():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	#include_router(app)
	#configure_static(app)
	create_tables()       #new
	return app





def getJWTPayload(token):
    # if we want to sign/encrypt the JSON object: {"hello": "world"}, we can do it as follows
    # encoded = jwt.encode({"hello": "world"}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    id: str = payload.get("id")
    # this is often used on the client side to encode the user's email address or other properties
    return id

def create_access_token(id,data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire,"id":id})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt



app = start_application()
