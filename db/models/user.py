from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_email_confirmed = Column(Boolean, default=True)
    todos = relationship("Todo", back_populates="owner")
