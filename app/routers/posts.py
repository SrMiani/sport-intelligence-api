# routers/posts.py — Endpoints de contenido
#
# POST /posts     → sube un post nuevo (requiere estar logueado)
# GET  /posts     → lista los posts más recientes
# GET  /posts/{id} → un post concreto

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token, oauth2_scheme

from app.core.database import get_db
from app.core.security import decode_token
from app.models.post import Post, ContentType
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["Contenido"])


# ── Helper: obtener el usuario actual desde el token ──

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


# ── Schemas ──

class CreatePostRequest(BaseModel):
    title: str
    content: str
    content_type: ContentType = ContentType.text

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    content_type: str
    loading_score: int
    author: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Endpoints ──

@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(
    data: CreatePostRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Sube un nuevo post a la plataforma.
    Requiere estar autenticado (token JWT en el header).
    """
    post = Post(
        title=data.title,
        content=data.content,
        content_type=data.content_type,
        author_id=current_user.id
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return {
        "message": "Post subido. El mundo lo verá.",
        "post_id": post.id,
        "loading_score": post.loading_score
    }


@router.get("", response_model=list[PostResponse])
def list_posts(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Devuelve los posts más recientes.
    skip y limit permiten paginar — de momento no hace falta que los toques.
    """
    posts = (
        db.query(Post)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        PostResponse(
            id=p.id,
            title=p.title,
            content=p.content,
            content_type=p.content_type.value,
            loading_score=p.loading_score,
            author=p.author.username,
            created_at=p.created_at
        )
        for p in posts
    ]


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Devuelve un post concreto por su ID."""
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        content_type=post.content_type.value,
        loading_score=post.loading_score,
        author=post.author.username,
        created_at=post.created_at
    )
