from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)): # Funçao recebe user_data(email, password) - dados enviados pelo user e o banco de dados
    existing_user = db.query(User).filter(User.email == user_data.email).first() 
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,             # verifica se o email já está sendo utlzado
            detail="Email already registered"
        )
    new_user = User(    # Cria um objeto User SQLAlchemy
        email=user_data.email,
        hashed_passwod=hash_password(user_data.password) # Hash da senha antes de salvar no banco. A senha pura nunca é salva. 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user # Response model controla o que va ser enviado de volta(Senha não vai ser enviada, por exemplo)

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user