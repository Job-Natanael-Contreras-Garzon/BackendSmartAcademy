# app/schemas/course.py
from pydantic import BaseModel, Field
from typing import Optional, List

class CourseBase(BaseModel):
    teacher_id: int
    subject_id: int
    group_id: Optional[int] = None
    period_id: Optional[int] = None
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    teacher_id: Optional[int] = None
    subject_id: Optional[int] = None
    group_id: Optional[int] = None
    period_id: Optional[int] = None
    description: Optional[str] = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        orm_mode = True

class CourseDetailResponse(CourseResponse):
    # Información adicional del profesor
    teacher_name: str
    # Información de la materia
    subject_name: str
    # Información del grupo si existe
    group_name: Optional[str] = None
    grade: Optional[str] = None
    level: Optional[str] = None
    # Información del periodo si existe
    period_name: Optional[str] = None