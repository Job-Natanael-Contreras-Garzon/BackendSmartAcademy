from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date
from enum import Enum

class AttendanceStatus(str, Enum):
    PRESENT = "presente"
    ABSENT = "ausente"
    LATE = "tarde"
    EXCUSED = "justificado"

class AttendanceBase(BaseModel):
    student_id: int
    course_id: int
    date: date
    status: AttendanceStatus
    notes: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None
    notes: Optional[str] = None

class AttendanceResponse(AttendanceBase):
    id: int

    class Config:
        orm_mode = True

class AttendanceDetailResponse(AttendanceResponse):
    # Información adicional del estudiante
    student_name: str
    student_code: str
    # Información del curso
    subject_name: str
    teacher_name: str
    # Información del grupo
    group_name: Optional[str] = None