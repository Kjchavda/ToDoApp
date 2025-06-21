from typing import Optional
from pydantic import BaseModel, EmailStr

class TodoCreate(BaseModel):
    title: str
    content: str
    completed: bool = False  
    tag_ids: list[int] = []

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    completed: bool = False 
    tag_ids: list[int] | None = None 


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

class TagOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class TagCreate(BaseModel):
    name: str


class TodoOut(BaseModel):
    id: int
    title: str
    content: str
    completed: bool
    tags: list[TagOut]

    class Config:
        orm_mode = True
