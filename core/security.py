from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import models, database
from database import get_db
from config import settings  # Import settings properly

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 token authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT Token
def create_access_token(data: dict, expires_delta: timedelta):
    """Generates a JWT access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  

# Decode JWT and Get Current User
def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    """Extracts user details from the JWT token and returns the authenticated user."""
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # ✅ Fixed
        email: str = payload.get("sub")
        role: str = payload.get("role")  # ✅ Extract user role from token

        if email is None or role is None:
            raise credentials_exception

        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception

