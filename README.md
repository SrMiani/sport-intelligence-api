Sport Intelligence API ⚡


Análisis de rendimiento deportivo con IA.




¿Qué hace?

Sport Intelligence API analiza el rendimiento deportivo usando IA. Describes tu actuación en texto — o subes contenido multimedia — y la IA evalúa tu técnica, detecta fortalezas y áreas de mejora, y te devuelve recomendaciones concretas para mejorar junto con una puntuación de rendimiento.


Stack


Python 3.12
FastAPI — framework web moderno y de alto rendimiento
OpenAI GPT-4o-mini — motor de análisis con IA
SQLAlchemy — ORM para gestión de base de datos
SQLite → PostgreSQL (producción)
JWT + bcrypt — autenticación segura
Uvicorn — servidor ASGI



Estructura del proyecto

sport-intelligence-api/
├── main.py                  # Punto de entrada
└── app/
    ├── core/
    │   ├── database.py      # Conexión y sesión de base de datos
    │   ├── security.py      # JWT y hash de contraseñas
    │   └── config.py        # Variables de entorno
    ├── models/
    │   ├── user.py          # Modelo de usuario
    │   └── analysis.py      # Modelo de análisis + Performance Score
    └── routers/
        ├── auth.py          # Registro e inicio de sesión
        └── analysis.py      # Endpoints de análisis + integración OpenAI


Funcionalidades

Autenticación


Registro de usuarios con hash de contraseña bcrypt
Login con JWT (token de 24h de duración)
Rutas protegidas mediante OAuth2 Bearer token


Análisis de rendimiento con IA


Describe tu actuación en lenguaje natural
Selecciona tu deporte y disciplina
Recibe feedback instantáneo con IA:

Performance Score (0-100)
Fortalezas detectadas en tu actuación
Áreas de mejora
Recomendaciones concretas para mejorar





Historial de rendimiento


Cada análisis se guarda con marca de tiempo
Seguimiento de tu progresión a lo largo del tiempo
Comparación de scores entre sesiones



Cómo empezar

1. Clona el repositorio

bashgit clone https://github.com/SrMiani/sport-intelligence-api.git
cd sport-intelligence-api

2. Crea y activa el entorno virtual

bashpython -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

3. Instala las dependencias

bashpip install fastapi uvicorn sqlalchemy pyjwt "passlib[bcrypt]" python-multipart bcrypt==4.0.1 email-validator openai python-dotenv

4. Configura las variables de entorno

Crea un archivo .env en la raíz del proyecto:

OPENAI_API_KEY=tu_api_key_de_openai

5. Arranca el servidor

bashuvicorn main:app --reload

6. Abre la documentación

http://localhost:8000/docs


Endpoints

MétodoEndpointAuthDescripciónPOST/auth/register❌Crear una cuenta nuevaPOST/auth/login❌Iniciar sesión y recibir token JWTPOST/analysis✅Analizar una actuación deportiva


Ejemplo de petición

jsonPOST /analysis
Authorization: Bearer <token>

{
    "sport": "fútbol",
    "discipline": "portero",
    "input_text": "Hoy entrené 1 hora. Mis reflejos estuvieron bien pero me costó en los balones aéreos y salir a despejar."
}

Ejemplo de respuesta

json{
    "id": 1,
    "sport": "fútbol",
    "discipline": "portero",
    "score": 70,
    "strengths": "Buenos reflejos durante el entrenamiento.",
    "improvements": "Dificultades con los balones aéreos y al salir a despejar.",
    "recommendations": "Practicar ejercicios de salto y posicionamiento para mejorar en balones aéreos, y simular despejes desde diferentes ángulos de ataque.",
    "created_at": "2026-07-01T23:48:39.009543"
}


Roadmap


 Autenticación de usuarios (JWT)
 Análisis de rendimiento con IA (texto)
 Performance Score (0-100)
 Historial de análisis por usuario
 Subida de vídeo y análisis por frames (OpenAI Vision)
 Criterios de evaluación específicos por deporte
 Gráficas de progresión
 Dashboard en React
 Containerización con Docker
 CI/CD con GitHub Actions
 Despliegue en GCP



Casos de uso


Atletas amateur que quieren feedback de nivel profesional sin necesidad de entrenador
Entrenadores personales que necesitan dar feedback remoto a múltiples clientes
Academias deportivas que quieren escalar el feedback individualizado
Apps de fitness que buscan añadir una capa de análisis con IA mediante API



Autor

Sergi Miani — AI Engineer, construyendo en la intersección entre deporte, datos e inteligencia artificial.

GitHub


Construido con FastAPI + OpenAI. Parte de un portfolio de herramientas con IA aplicada.