import datetime
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(max_length=12)


class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True


class CheckinCreate(BaseModel):
    user_id: int
    status: str


class Checkin(CheckinCreate):
    checkin_id: int
    create_date: datetime.datetime


    class Config:
        orm_mode = True



