from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Read
@app.get("/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db:Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/checkin/", response_model=List[schemas.Checkin])
async def read_checkin(skip: int = 0, limit: int = 100, user_id: int = 1, db:Session = Depends(get_db)):
    checkin = crud.get_checkin(db, skip=skip, limit=limit, user_id=user_id)
    return checkin


# Create
@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/checkin", response_model=schemas.Checkin)
async def create_checkin(checkin: schemas.CheckinCreate, db: Session = Depends(get_db)):
    return crud.create_checkin(db=db, checkin=checkin)


# delete
@app.post("/users_delete", response_model=schemas.UserCreate)
async def delete_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user=user)