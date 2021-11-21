from datetime import datetime

from pydantic import BaseModel

from schemas.user import UserResponse


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
