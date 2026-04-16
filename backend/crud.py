from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Post
from schemas import PostCreate, PostUpdate
from typing import List, Optional, Tuple
import math


def get_post(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10) -> List[Post]:
    return db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()


def get_paginated_posts(db: Session, page: int = 1, page_size: int = 3) -> Tuple[List[Post], int, int]:
    query = db.query(Post).order_by(Post.created_at.desc())
    total = query.count()
    total_pages = math.ceil(total / page_size)
    skip = (page - 1) * page_size
    posts = query.offset(skip).limit(page_size).all()
    return posts, total, total_pages


def search_posts(db: Session, keyword: str, page: int = 1, page_size: int = 10) -> Tuple[List[Post], int, int]:
    query = db.query(Post).filter(
        or_(
            Post.title.ilike(f"%{keyword}%"),
            Post.content.ilike(f"%{keyword}%"),
            Post.tags.ilike(f"%{keyword}%")
        )
    ).order_by(Post.created_at.desc())
    total = query.count()
    total_pages = math.ceil(total / page_size)
    skip = (page - 1) * page_size
    posts = query.offset(skip).limit(page_size).all()
    return posts, total, total_pages


def create_post(db: Session, post: PostCreate) -> Post:
    db_post = Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post: PostUpdate) -> Optional[Post]:
    db_post = get_post(db, post_id)
    if db_post:
        update_data = post.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_post, field, value)
        db.commit()
        db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> bool:
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False
