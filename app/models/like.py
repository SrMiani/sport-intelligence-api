# models/like.py — El modelo Post
#
# Un post es cualquier pieza de contenido que sube un usuario.
# De momento solo tiene texto. Luego añadiremos imágenes, vídeos, etc.

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean



from datetime import datetime
from app.core.database import Base





class Like(Base):
    __tablename__ = "likes"

    id           = Column(Integer, primary_key=True, index=True)
    post_id      = Column(Integer, ForeignKey("posts.id"), nullable=False)
    is_superlike = Column(Boolean, default=False)
    created_at   = Column(DateTime, default=datetime.utcnow)

    # Clave foránea — cada like pertenece a un usuario
    # ForeignKey le dice a SQLite: "este número tiene que existir en users.id"
    author_id    = Column(Integer, ForeignKey("users.id"), nullable=False)

    

    def __repr__(self):
        return f"<Liked {self.id} by user {self.author_id}>"
