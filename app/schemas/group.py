from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

# Enumeraciones para campos específicos
class GradeEnum(str, Enum):
    PREKINDER = "prekinder"
    KINDER = "kinder"
    PRIMERO = "1ro"
    SEGUNDO = "2do"
    TERCERO = "3ro"
    CUARTO = "4to"
    QUINTO = "5to"
    SEXTO = "6to"

class LevelEnum(str, Enum):
    INICIAL = "inicial"
    PRIMARIA = "primaria"
    SECUNDARIA = "secundaria"

# Esquemas base para grupo
class GroupBase(BaseModel):
    grade: GradeEnum
    level: LevelEnum
    group_name: str  # A, B, C, etc.

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    grade: Optional[GradeEnum] = None
    level: Optional[LevelEnum] = None
    group_name: Optional[str] = None

class GroupResponse(GroupBase):
    id: int

    class Config:
        orm_mode = True
