from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from .role import RoleResponse as RoleSchemaResponse # Import RoleResponse
from datetime import datetime, date
from enum import Enum

# Enumeraciones para campos específicos
class GenderEnum(str, Enum):
    FEMALE = "FEMALE"
    MALE = "MALE"
    OTHER = "OTHER"

class RoleEnum(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    PARENT = "PARENT"
    ADMINISTRATOR = "ADMINISTRATOR"

# Esquemas base para usuario
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    
class UserCreate(UserBase):
    password: str
    phone: Optional[str] = None
    direction: Optional[str] = None
    birth_date: Optional[date] = None  # Changed from str to date
    gender: Optional[GenderEnum] = GenderEnum.OTHER
    role: Optional[RoleEnum] = RoleEnum.STUDENT
    is_superuser: Optional[bool] = False

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None
    birth_date: Optional[date] = None  # Changed from str to date
    gender: Optional[GenderEnum] = None
    photo: Optional[str] = None  # Puede ser una URL como string
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None  # Added is_superuser
    role: Optional[RoleEnum] = None

class UserResponse(UserBase):
    id: int
    phone: Optional[str] = None
    direction: Optional[str] = None
    birth_date: Optional[date] = None  # Changed from str to date
    gender: GenderEnum
    role: RoleSchemaResponse # Use RoleResponse schema for nested role details
    photo: Optional[str] = None
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

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