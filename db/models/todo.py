from sqlalchemy import Boolean, Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")