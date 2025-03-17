from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas
from database import get_db
from core.security import create_access_token, verify_password, hash_password, get_current_user
from config import settings


router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    **Public Route**  
    - Allows **new users to register**.  
    - Default role is **user** unless specified.
    """
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # create user object without passing `role` explicitly
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),  # ✅ Hash password
        role=user_data.role  # ✅ This now correctly uses default or provided value
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# User Login (Open Access)
@router.post("/login", response_model=schemas.TokenResponse)
def login_user(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    **Public Route**  
    - Users and admins can **log in** and receive a JWT token.
    """
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, 
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

