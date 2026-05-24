# security.py — Contraseñas y tokens JWT
#
# JWT (JSON Web Token): cuando un usuario se loguea correctamente,
# le damos un "token" — una cadena de texto encriptada.
# Ese token es como su pulsera de evento: lo lleva siempre
# y se lo muestra a la API para demostrar que es quien dice ser.
# No hace falta que vuelva a poner contraseña en cada petición.

from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import jwt

# Clave secreta para firmar los tokens. 
# En producción esto iría en variables de entorno, nunca en el código.
SECRET_KEY = "loading-secret-key-cambiar-en-produccion"
ALGORITHM = "HS256"           # Algoritmo de encriptación
TOKEN_EXPIRE_MINUTES = 60 * 24  # El token dura 24 horas

# CryptContext gestiona el hash de contraseñas con bcrypt
# Nunca guardamos la contraseña real — solo su "huella" encriptada
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Convierte una contraseña en texto a su versión encriptada."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Comprueba si una contraseña coincide con su versión encriptada."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    """
    Crea un token JWT para un usuario.
    El token contiene: el ID del usuario y cuándo expira.
    """
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),   # sub = subject (quién es el usuario)
        "exp": expire           # exp = cuándo expira el token
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> int | None:
    """
    Decodifica un token y devuelve el ID del usuario.
    Si el token es inválido o ha expirado, devuelve None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except jwt.ExpiredSignatureError:
        return None  # Token caducado
    except jwt.InvalidTokenError:
        return None  # Token inválido



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")