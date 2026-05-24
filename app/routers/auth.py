# routers/auth.py — Endpoints de autenticación
#
# Aquí viven dos endpoints:
# POST /auth/register → crea una cuenta nueva
# POST /auth/login    → entra con email y contraseña, recibe un token

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User

# APIRouter es como un "mini-app" que luego enchufamos al app principal
router = APIRouter(prefix="/auth", tags=["Autenticación"])


# ── Schemas ──
# Pydantic valida automáticamente los datos que llegan.
# Si falta un campo o el email no es válido, FastAPI devuelve error claro.

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr  # Valida que sea un email real
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


# ── Endpoints ──

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Crea una cuenta nueva en Loading.
    Comprueba que el username y email no estén ya en uso.
    """
    # ¿Ya existe ese username?
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ese username ya está en uso"
        )

    # ¿Ya existe ese email?
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ese email ya está registrado"
        )

    # Creamos el usuario — la contraseña se guarda hasheada, nunca en texto plano
    new_user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"Bienvenido a Loading, {new_user.username}. Empieza a cargar."}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login con email y contraseña.
    Si todo es correcto, devuelve un token JWT.
    """
    # Buscamos el usuario por email
    user = db.query(User).filter(User.email == data.email).first()

    # Si no existe o la contraseña no coincide — mismo error (seguridad)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    # Generamos el token
    token = create_access_token(user.id)

    return TokenResponse(
        access_token=token,
        username=user.username
    )
