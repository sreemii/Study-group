from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext
import enum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)

# Token Schemas
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = "user"

# User Schemas

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  
    role: Optional[UserRole] = UserRole.user

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

# Study Group Schemas
class StudyGroupCreate(BaseModel):
    name: str
    description: Optional[str] = None

class StudyGroupResponse(StudyGroupCreate):
    id: int

    class Config:
        from_attributes = True

# Group Member Schema
class GroupMemberCreate(BaseModel):
    user_id: int
    group_id: int

class GroupMemberResponse(BaseModel):
    id: int
    user_id: int
    group_id: int

# Study Session Schemas
class StudySessionCreate(BaseModel):
    group_id: int
    scheduled_time: datetime
    

class StudySessionUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    

class StudySessionResponse(BaseModel):
    id: int
    group_id: int
    scheduled_time: datetime
    

    class Config:
        from_attributes = True  

# Resource Schemas
class ResourceCreate(BaseModel):
    group_id: int
    title: str
    url: str

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None  

class ResourceResponse(BaseModel):
    id: int
    group_id: int
    title: str
    url: str

    class Config:
        from_attributes = True
