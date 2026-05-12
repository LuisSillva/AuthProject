from fastapi import FastAPI
from app.database import engine, Base
from app.routers.auth import router as auth_router
import app.models.user  # Base.metadata.create_all só consegue criar tables de models que o SQLAlchemy conhece. SQLAlchemy reconhece um model quando o mesmo é importado
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auth System")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)