from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import decode_token, oauth2_scheme
from app.models.analysis import Analysis
from app.models.user import User
from openai import OpenAI
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter(prefix="/analysis", tags=["Analysis"])


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


class AnalysisRequest(BaseModel):
    sport: str
    discipline: str
    input_text: str


@router.post("")
def create_analysis(
    data: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Construimos el prompt — aquí está nuestra magia
    prompt = f"""
    Eres un analista deportivo experto en rendimiento amateur y semiprofesional.
    
    El atleta practica {data.sport}, disciplina: {data.discipline}.
    
    Descripción de su actuación:
    {data.input_text}
    
    Analiza esta actuación y responde ÚNICAMENTE con un JSON con esta estructura exacta:
    {{
        "score": <número del 0 al 100>,
        "strengths": "<puntos fuertes detectados>",
        "improvements": "<áreas de mejora>",
        "recommendations": "<recomendaciones concretas para mejorar>"
    }}
    
    No añadas texto fuera del JSON.
    """

    # Llamada a OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extraemos el texto de la respuesta
    result_text = response.choices[0].message.content

    # Limpiamos el texto por si OpenAI añade markdown
    result_text = result_text.strip()
    if result_text.startswith("```"):
        result_text = result_text.split("```")[1]
    if result_text.startswith("json"):
        result_text = result_text[4:]
    result_text = result_text.strip()

    # Convertimos el JSON de texto a diccionario Python
    import json
    result = json.loads(result_text)

    if result["score"] > 80:
        result["strengths"] = "ELITE - " + result["strengths"]
    # Guardamos en la base de datos
    analysis = Analysis(
        user_id=current_user.id,
        sport=data.sport,
        discipline=data.discipline,
        input_text=data.input_text,
        score=result["score"],
        strengths=result["strengths"],
        improvements=result["improvements"],
        recommendations=result["recommendations"]
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return {
        "id": analysis.id,
        "sport": analysis.sport,
        "discipline": analysis.discipline,
        "score": analysis.score,
        "strengths": analysis.strengths,
        "improvements": analysis.improvements,
        "recommendations": analysis.recommendations,
        "created_at": analysis.created_at
    }