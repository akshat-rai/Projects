from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model
from .database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True


retry = 1
while retry <= 3:
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="fastapi",
            user="postgres",
            password="Hellyeah@123",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connection to database established!")
        break
    except Exception as e:
        retry += 1
        print("Connection to database failed!")
        print(e)
        time.sleep(2)

my_posts = [
    {
        "post_id": 1,
        "title": "My First Post title",
        "body": "My First Post Body",
    },
    {
        "post_id": 2,
        "title": "My Second Post title",
        "body": "My Second Post Body",
    },
]


def find_post(id):
    for i, post in enumerate(my_posts):
        if post.get("post_id") == id:
            return {"index": i, "post": post}
    return {"index": -1, "post": None}


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/posts")
def get_all_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostModel):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    created_post = cursor.fetchone()
    conn.commit()
    return {"data": created_post}


@app.get("/posts/{id}")
def get_post_via_id(id: int):
    cursor.execute(""" SELECT * FROM posts where id = %s""", str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post_id {id} not found!",
        )
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    post = cursor.fetchone()

    conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exists!",
        )


@app.put("/posts/{id}")
def update_post(id: int, post: PostModel):
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
        (post.title, post.content, post.published, id),
    )
    post = cursor.fetchone()

    conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exists!",
        )

    return {"data": post}
