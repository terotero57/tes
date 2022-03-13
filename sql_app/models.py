from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    checkin = relationship("Checkin", cascade = "all, delete, delete-orphan")


class Checkin(Base):
    __tablename__ = 'checkin'
    checkin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(String)




