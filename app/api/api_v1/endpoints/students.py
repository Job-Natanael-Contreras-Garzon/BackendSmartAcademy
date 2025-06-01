from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.student import Student as StudentSchema, StudentCreate
from app.services.student_service import (
    get_student, get_students, create_student, 
    update_student, delete_student
)
from app.config.database import get_db
from app.services.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[StudentSchema])
def read_students(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    students = get_students(db, skip=skip, limit=limit)
    return students

@router.post("/", response_model=StudentSchema, status_code=status.HTTP_201_CREATED)
def create_student_endpoint(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return create_student(db=db, student=student)

@router.get("/{student_id}", response_model=StudentSchema)
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_student = get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_student

@router.put("/{student_id}", response_model=StudentSchema)
def update_student_endpoint(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_student = update_student(db, student_id=student_id, student_update=student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_endpoint(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not delete_student(db, student_id=student_id):
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return None