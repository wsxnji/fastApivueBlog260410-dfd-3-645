from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Post
from schemas import PostCreate, PostUpdate
from typing import List, Optional


def get_post(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10) -> List[Post]:
    return db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()


def get_posts_with_pagination(db: Session, page: int = 1, page_size: int = 3, category: str = None, search: str = None):
    query = db.query(Post)
    
    # 分类筛选
    if category and category != "全部":
        query = query.filter(Post.category == category)
    
    # 搜索功能
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Post.title.ilike(search_pattern)) |
            (Post.content.ilike(search_pattern)) |
            (Post.tags.ilike(search_pattern))
        )
    
    total = query.count()
    posts = query.order_by(Post.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "posts": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


def get_posts_count(db: Session) -> int:
    return db.query(func.count(Post.id)).scalar()


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


def get_categories(db: Session) -> List[str]:
    categories = db.query(Post.category).distinct().all()
    return [c[0] for c in categories if c[0]]


def get_all_tags(db: Session) -> List[str]:
    all_tags = []
    posts_with_tags = db.query(Post.tags).filter(Post.tags != "").all()
    for tags_str in posts_with_tags:
        if tags_str[0]:
            tags = [tag.strip() for tag in tags_str[0].split(",") if tag.strip()]
            all_tags.extend(tags)
    return list(set(all_tags))
