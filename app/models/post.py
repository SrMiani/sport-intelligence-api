# models/post.py — El modelo Post
#
# Un post es cualquier pieza de contenido que sube un usuario.
# De momento solo tiene texto. Luego añadiremos imágenes, vídeos, etc.

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class ContentType(str, enum.Enum):
    """Tipo de contenido — lo ampliaremos con video, imagen, etc."""
    text  = "text"
    image = "image"
    video = "video"


class Post(Base):
    __tablename__ = "posts"

    id           = Column(Integer, primary_key=True, index=True)
    title        = Column(String, nullable=False)
    content      = Column(String, nullable=False)
    content_type = Column(Enum(ContentType), default=ContentType.text)
    
    # El Loading Score — empieza en 0, lo calcularemos después
    likes_score = Column(Integer, default=0, nullable=False)
    superlikes_score = Column(Integer, default=0, nullable=False)
    
    # Cuándo se creó
    created_at   = Column(DateTime, default=datetime.utcnow)

    # Clave foránea — cada post pertenece a un usuario
    # ForeignKey le dice a SQLite: "este número tiene que existir en users.id"
    author_id    = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relación inversa: desde el post podemos acceder a su autor
    author = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post {self.id} by user {self.author_id}>"
