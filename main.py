from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import auth
from app.models.user import User
from app.models.analysis import Analysis
from app.routers import analysis
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sport Intelligence API",
    description="AI-powered sport performance analysis. Upload a video or describe your performance and get instant feedback.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(analysis.router)



@app.get("/")
def root():
    return {
        "name": "Sport Intelligence API",
        "version": "0.1.0",
        "status": "online",
        "docs": "/docs"
    }