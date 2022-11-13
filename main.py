from datetime import timedelta , date , datetime
from typing import Union
from fastapi import FastAPI
import jwt
from core.config import settings
from db.session import engine   #new
from db.base import Base
from db.utils import check_db_connected , check_db_disconnected
from apis.base import api_router
JWT_SECRET :str = "secret_key" # IRL we should NEVER hardcode the secret: it should be an evironment variable!!!
JWT_ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


def create_tables():           #new
	Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)

def start_application():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	#include_router(app)
	#configure_static(app)
	create_tables()       #new
	return app



app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
    
    
