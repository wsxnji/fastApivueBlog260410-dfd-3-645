from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from crud import (
    get_post, get_posts, get_posts_with_pagination, create_post, 
    update_post, delete_post, get_categories, get_all_tags
)
from schemas import Post, PostCreate, PostUpdate, PostListResponse

router = APIRouter()


@router.get("/posts", response_model=PostListResponse)
def read_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=100),
    category: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    result = get_posts_with_pagination(db, page=page, page_size=page_size, category=category, search=search)
    return result


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


@router.get("/categories")
def read_categories(db: Session = Depends(get_db)):
    categories = get_categories(db)
    return {"categories": categories}


@router.get("/tags")
def read_tags(db: Session = Depends(get_db)):
    tags = get_all_tags(db)
    return {"tags": tags}
