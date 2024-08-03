from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_items_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = get_items_by_id(db, item_id)
    if db_item is None:
        return
    db.delete(db_item)
    db.commit()
    return db_item


def create_privelige(db: Session, privelige: schemas.PriveligeCreate, user_id: int, item_id: int):
    db_privelige = models.Privelige(**privelige.model_dump(), item_id = item_id, user_id = user_id)
    db.add(db_privelige)
    db.commit()
    db.refresh(db_privelige)
    return db_privelige


def get_privelige_by_item_id(db: Session, item_id: int):
    return db.query(models.Privelige).filter(models.Privelige.item_id == item_id).first()


def delete_privelige(db: Session, item_id: int):
    db_privelige = get_privelige_by_item_id(db, item_id)
    if db_privelige is None:
        return
    db.delete(db_privelige)
    db.commit()
    return db_privelige