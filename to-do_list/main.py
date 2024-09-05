from fastapi import Depends, FastAPI, HTTPException
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


@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/login", response_model=schemas.User)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    verify_user = crud.login_user(db, user)
    if verify_user is None:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return verify_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/items/{user_id}", response_model=[schemas.Item])
def read_item_by_user(user_id: int, db: Session = Depends(get_db)):
    db_items = crud.get_items_by_user(db, user_id=user_id)
    if db_items is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_items


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item_by_id(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_items_by_id(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.post("/users/{user_id}/item_edit/", response_model=schemas.Item)
def edit_item_for_user(
    user_id: int, item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.post("/users/{user_id}/priveliges/", response_model=schemas.Privelige)
def create_privelige(
    user_id: int,
    privelige: schemas.PriveligeCreate,
    for_user_id: int,
    item_id: int,
    db: Session = Depends(get_db),
):
    db_user = crud.get_user(db, user_id=for_user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    items = crud.get_items_by_id(db, item_id=item_id)
    if items is None:
        raise HTTPException(status_code=404, detail="Item not found!")
    if items.owner_id != user_id:
        raise HTTPException(
            status_code=404, detail="You must be owner to create privelige!"
        )
    return crud.create_privelige(
        db, privelige=privelige, user_id=for_user_id, item_id=item_id
    )


@app.delete("/users/{user_id}/delete_privelige/", response_model=schemas.Privelige)
def delete_privelige(item_id: int, db: Session = Depends(get_db)):
    db_privelige = crud.delete_privelige(db, item_id=item_id)
    if db_privelige is None:
        raise HTTPException(status_code=404, detail="Privelige not found")
    return db_privelige
