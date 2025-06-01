from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum

class StudentStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    GRADUATED = "graduated"

class StudentBase(BaseModel):
    user_id: int
    group_id: Optional[int] = None
    status: StudentStatusEnum = StudentStatusEnum.ACTIVE
    student_code: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    group_id: Optional[int] = None
    status: Optional[StudentStatusEnum] = None
    student_code: Optional[str] = None

class StudentResponse(StudentBase):
    id: int

    class Config:
        orm_mode = True

class StudentDetailResponse(StudentResponse):
    # Campos adicionales del usuario vinculado
    full_name: str
    email: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    photo: Optional[str] = None
    # Campos del grupo si existe
    grade: Optional[str] = None
    level: Optional[str] = None
    group_name: Optional[str] = None