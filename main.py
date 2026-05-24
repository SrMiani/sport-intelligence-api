# main.py — El punto de entrada de la API
#
# Este es el archivo que arranca todo. Uvicorn lo lee y levanta el servidor.

from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import auth, posts
from app.models.like import Like
from app.routers import likes

# Creamos todas las tablas en la base de datos al arrancar
# Si ya existen, no las toca — no borra datos
Base.metadata.create_all(bind=engine)

# La aplicación
app = FastAPI(
    title="Loading API",
    description="La plataforma de talento y competición. El momento antes de todo.",
    version="0.1.0"
)

# Enchufamos los routers
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(likes.router)


@app.get("/")
def root():
    return {
        "name": "Loading API",
        "version": "0.1.0",
        "status": "online",
        "docs": "/docs"
    }
