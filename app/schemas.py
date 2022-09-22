from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional
from pydantic.types import conint

class Post(BaseModel):
    title : str
    Content : str
    published : bool = True
    rating : Optional[int] = 0

class updatedPost(BaseModel):
    title : str = ''
    Content : str = ''
    published : bool = True
    rating : Optional[int] = 0

class Userout(BaseModel):
    id: int
    email: str
    created_at : datetime

    class Config:
        orm_mode = True

class Postout(BaseModel):
    id: int
    title: str
    Content: str
    published: bool
    rating: int
    created_at: datetime
    owner_id: int
    owner: Userout

    class Config:
        orm_mode = True

class PostAllOut(BaseModel):
    Post: Postout
    Votes: int

    class Config:
        orm_mode = True

class user(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class vote(BaseModel):
    post_id:int
    dir: conint(le=1)