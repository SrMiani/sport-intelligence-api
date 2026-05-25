# models/user.py — El modelo Usuario
#
# Un modelo es la representación de una tabla en la base de datos.
# Esta clase le dice a SQLAlchemy:
# "Crea una tabla llamada 'users' con estas columnas."

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"  # Nombre de la tabla en la base de datos

    # Columnas de la tabla
    id           = Column(Integer, primary_key=True, index=True)
    username     = Column(String, unique=True, index=True, nullable=False)
    email        = Column(String, unique=True, index=True, nullable=False)
    password     = Column(String, nullable=False)  # Guardamos el hash, nunca la contraseña real
    bio          = Column(String, default="")
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    superlikes_available = Column(Integer, default=1)  # Número de superlikes disponibles

    # Relación: un usuario puede tener muchos posts
    # Esto nos permite hacer user.posts y obtener todos sus posts
    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"<User {self.username}>"
