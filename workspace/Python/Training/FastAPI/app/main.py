from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/posts", response_model=List[schemas.PostResposneModel])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(model.PostModel).all()
    return posts


@app.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResposneModel,
)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = model.PostModel(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResposneModel)
def get_post_via_id(id: int, db: Session = Depends(get_db)):
    post = db.query(model.PostModel).filter(model.PostModel.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post_id {id} not found!",
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.PostModel).filter(model.PostModel.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exists!",
        )

    post.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{id}", response_model=schemas.PostResposneModel)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):
    updated_post = db.query(model.PostModel).filter(model.PostModel.id == id)
    if not updated_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exists!",
        )
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return updated_post.first()


@app.get(
    "/users",
    response_model=List[schemas.UserResposneModel],
)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(model.UserModel).all()
    return users


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResposneModel,
)
def create_user(user: schemas.UserModel, db: Session = Depends(get_db)):
    new_user = model.UserModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
