# database.py — La conexión a la base de datos
# SQLAlchemy es la librería que nos permite hablar con SQLite desde Python
# sin escribir SQL directamente. Escribimos Python y ella lo traduce.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# La "dirección" de nuestra base de datos. 
# sqlite:/// significa que es un archivo local.
# loading.db es el archivo que se creará en la carpeta del proyecto.
DATABASE_URL = "sqlite:///./loading.db"

# El motor — es la conexión real a la base de datos
# check_same_thread=False es necesario para SQLite con FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal — cada vez que alguien hace una petición a la API,
# abrimos una "sesión" con la base de datos y la cerramos al terminar
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base — todos nuestros modelos (User, Post...) heredarán de aquí
Base = declarative_base()

# Esta función la usaremos en cada endpoint para obtener la sesión
# y asegurarnos de que siempre se cierra correctamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
