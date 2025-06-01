from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.models.student import Student
from app.schemas.student import StudentCreate, Student as StudentSchema

def get_student(db: Session, student_id: int) -> Optional[Student]:
    return db.query(Student).filter(Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
    return db.query(Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: StudentCreate) -> Student:
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student_update: StudentCreate) -> Optional[Student]:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        for key, value in student_update.dict().items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int) -> bool:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False