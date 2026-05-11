from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import decode_access_token
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # extrai o token jwt do authorization header. OAuth22 precisa saber o endpoint que vai gerar o token.
def get_db(): # Abre e fecha o banco de dados automaticamente
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
        token: str = Depends(oauth2_scheme), # pega o token antes de executar a funcao
        db: Session = Depends(get_db) # abre o banco de dados
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",                # mensagem padrao de exception
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_access_token(token) # Se válido, retorna payload
    if token_data is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    
    return user # Retorna tudo do User(Model user.py)
