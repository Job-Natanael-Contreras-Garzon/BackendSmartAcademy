# app/api/api_v1/endpoints/courses.py
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse
from app.core.security import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve courses.
    """
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    *,
    db: Session = Depends(get_db),
    course_in: CourseCreate,
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Create new course.
    """
    course = Course(
        name=course_in.name,
        description=course_in.description,
        credits=course_in.credits
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Get course by ID.
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course