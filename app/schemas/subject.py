from pydantic import BaseModel
from typing import Optional, List

class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class SubjectResponse(SubjectBase):
    id: int

    class Config:
        orm_mode = True
