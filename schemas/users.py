from pydantic import BaseModel
from pydantic import EmailStr


#properties required during user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password : str
    
class ShowUser(BaseModel):
    username: str
    email: EmailStr
    jwt : str
