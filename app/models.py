## модели SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True, index = True, nullable = False)
    email = Column(String, unique = True, index = True, nullable = False)
    password = Column(String, nullable = False)
    
    items = relationship('Item', back_populates = 'owner', cascade = 'all, delete')


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    description = Column(String, nullable = True)

    owner_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'))
    owner = relationship('User', back_populates = 'items')

    create_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), server_default = func.now(), onupdate = func.now())





