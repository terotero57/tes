from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import desc


# ユーザー一覧
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# チェックイン時間検索
def get_checkin(db: Session, skip: int = 0, limit: int = 10, user_id: int = 1):
    return db.query(models.Checkin).\
        filter(models.Checkin.user_id == user_id). \
        order_by(desc(models.Checkin.checkin_id)). \
        offset(skip).\
        limit(limit).\
        all()


# ユーザー登録
def create_user(db: Session, user: schemas.User):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ユーザー削除
def delete_user(db: Session, user: schemas.User):
    delete = db.query(models.User).filter(models.User.username == user.username).one()
    db.delete(delete)
    db.commit()
    return {"username": user.username}




# チェックイン実施
def create_checkin(db: Session, checkin: schemas.Checkin):
    db_checkin = models.Checkin(user_id=checkin.user_id, status=checkin.status)
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin