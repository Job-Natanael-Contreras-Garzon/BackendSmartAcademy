from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

# Enumeraciones para campos específicos
class GenderEnum(str, Enum):
    FEMALE = "female"
    MALE = "male"
    OTHER = "other"

class RoleEnum(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"
    ADMINISTRATOR = "administrator"

# Esquemas base para usuario
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    
class UserCreate(UserBase):
    password: str
    phone: Optional[str] = None
    direction: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[GenderEnum] = GenderEnum.OTHER
    role: Optional[RoleEnum] = RoleEnum.STUDENT
    is_superuser: Optional[bool] = False

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[GenderEnum] = None
    photo: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    phone: Optional[str] = None
    direction: Optional[str] = None
    birth_date: Optional[str] = None
    gender: GenderEnum
    role: RoleEnum
    photo: Optional[str] = None
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True

# Esquemas para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    full_name: str
    role: str
    is_superuser: bool

class TokenData(BaseModel):
    email: Optional[str] = None

# Esquema para cambio de contraseña
class PasswordChange(BaseModel):
    current_password: str
    new_password: str