from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class TeacherStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"

class TeacherBase(BaseModel):
    user_id: int
    specialization: Optional[str] = None
    status: TeacherStatusEnum = TeacherStatusEnum.ACTIVE
    teacher_code: str

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    specialization: Optional[str] = None
    status: Optional[TeacherStatusEnum] = None
    teacher_code: Optional[str] = None

class TeacherResponse(TeacherBase):
    id: int

    class Config:
        orm_mode = True

class TeacherDetailResponse(TeacherResponse):
    # Campos adicionales del usuario vinculado
    full_name: str
    email: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    photo: Optional[str] = None
