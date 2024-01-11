from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostModel):
    pass


class UserModel(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str
    username: str


class PostResposneModel(PostModel):
    created_at: datetime

    class Config:
        orm_model = True


class UserResposneModel(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    username: str
    created_at: datetime

    class Config:
        orm_model = True
