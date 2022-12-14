from pydantic import BaseModel
from pydantic import Required


#properties required during user creation
class TodoCreate(BaseModel):
    title: str
    description: str
    
    
class TodoUpdate(BaseModel):
    id: str
    title: str
    description: str
    complete: bool