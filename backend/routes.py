from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from crud import get_post, get_posts, get_posts_count, create_post, update_post, delete_post
from schemas import Post, PostCreate, PostUpdate
from typing import Optional

router = APIRouter()


@router.get("/posts")
def read_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    posts = get_posts(db, skip=skip, limit=page_size, search=search, category=category, tag=tag)
    total = get_posts_count(db, search=search, category=category, tag=tag)
    return {
        "posts": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


@router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.post("/posts", response_model=Post)
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db=db, post=post)


@router.put("/posts/{post_id}", response_model=Post)
def update_existing_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = update_post(db=db, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.delete("/posts/{post_id}")
def delete_existing_post(post_id: int, db: Session = Depends(get_db)):
    success = delete_post(db=db, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}