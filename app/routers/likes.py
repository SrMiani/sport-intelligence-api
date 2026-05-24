# routers/likes.py — Endpoints de contenido
#


from app.models.like import Like
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.core.security import decode_token
from app.models.post import Post, ContentType
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token, oauth2_scheme

router = APIRouter(prefix="/posts", tags=["Likes"])


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






# ── Endpoints ──

@router.post("/{post_id}/like")
def give_like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)    
):
    
     # Check if post exists before liking
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="El post no existe")
    

    #Comprobar que el usuario no haya dado like ya
    like = db.query(Like).filter(Like.post_id == post_id, Like.author_id == current_user.id).first()
    if like:
        raise HTTPException(status_code=400, detail="Ya has dado like a este post")

    

    new_like = Like(post_id=post_id, author_id=current_user.id)
    db.add(new_like)
    db.commit()

    post.loading_score += 1
    db.commit()
    db.refresh(post)
    


    return {
    "message": "Like dado",
    "post_id": post_id,
    "user": current_user.username,
    "loading_score": post.loading_score
    
     }


