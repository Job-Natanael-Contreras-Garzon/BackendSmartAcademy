from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date

class GradeBase(BaseModel):
    student_id: int
    course_id: int
    period: str
    value: float = Field(ge=0.0, le=100.0)  # Nota entre 0 y 100
    date_recorded: Optional[date] = None

class GradeCreate(GradeBase):
    @validator('value')
    def validate_grade_value(cls, v):
        if v < 0 or v > 100:
            raise ValueError('La calificación debe estar entre 0 y 100')
        return v

class GradeUpdate(BaseModel):
    value: Optional[float] = Field(None, ge=0.0, le=100.0)
    period: Optional[str] = None
    date_recorded: Optional[date] = None
    
    @validator('value')
    def validate_grade_value(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('La calificación debe estar entre 0 y 100')
        return v

class GradeResponse(GradeBase):
    id: int

    class Config:
        orm_mode = True

class GradeDetailResponse(GradeResponse):
    # Información adicional del estudiante
    student_name: str
    student_code: str
    # Información del curso
    subject_name: str
    teacher_name: str
    # Información del grupo
    group_name: Optional[str] = None