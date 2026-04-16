from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    summary: Optional[str] = None
    category: Optional[str] = '其它'
    tags: Optional[str] = ''


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None


class Post(PostBase):
    id: int
    summary: Optional[str] = None
    category: Optional[str] = '其它'
    tags: Optional[str] = ''
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True