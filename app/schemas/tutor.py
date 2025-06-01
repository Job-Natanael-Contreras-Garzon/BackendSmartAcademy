from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class RelationshipType(str, Enum):
    """Tipos de relación entre tutor y estudiante"""
    TUTOR = "tutor"
    PARENT = "parent"
    PARTNER = "partner"
    OTHER = "other"


class TutorStudentBase(BaseModel):
    """Esquema base para relación tutor-estudiante"""
    student_id: int
    user_id: int  # ID del usuario que será tutor
    relationship: RelationshipType
    notes: Optional[str] = None


class TutorStudentCreate(TutorStudentBase):
    """Esquema para crear relación tutor-estudiante"""
    pass


class TutorStudentUpdate(BaseModel):
    """Esquema para actualizar relación tutor-estudiante"""
    relationship: Optional[RelationshipType] = None
    notes: Optional[str] = None


class TutorStudentResponse(TutorStudentBase):
    """Esquema para respuesta de relación tutor-estudiante"""
    id: int

    class Config:
        from_attributes = True


class TutorStudentDetailResponse(TutorStudentResponse):
    """Esquema para respuesta detallada de relación tutor-estudiante"""
    student_name: str
    tutor_name: str
    tutor_email: str
    tutor_phone: Optional[str] = None
