# app/schemas/course.py
from pydantic import BaseModel, Field
from typing import Optional

class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    credits: int = Field(gt=0)

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int

    class Config:
        orm_mode = True