# app/api/api_v1/endpoints/dashboard.py
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.config.database import get_db
from app.core.security import get_current_active_user
from app.models.student import Student
from app.models.grade import Grade
from app.models.attendance import Attendance
from app.models.participation import Participation
from app.services.ml_service import MLService

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Obtiene estadísticas generales para el dashboard.
    """
    # Contar estudiantes
    student_count = db.query(func.count(Student.id)).scalar()
    
    # Promedio general de notas
    avg_grade = db.query(func.avg(Grade.value)).scalar() or 0
    
    # Promedio de asistencia
    attendance_rate = db.query(func.avg(Attendance.presence)).scalar() or 0
    attendance_percentage = attendance_rate * 100
    
    # Promedio de participación
    avg_participation = db.query(func.avg(Participation.score)).scalar() or 0
    
    return {
        "total_students": student_count,
        "average_grade": float(avg_grade),
        "attendance_percentage": float(attendance_percentage),
        "average_participation": float(avg_participation)
    }

@router.get("/student/{student_id}")
def get_student_dashboard(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Obtiene estadísticas de un estudiante específico.
    """
    # Verificar si el estudiante existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return {"error": "Estudiante no encontrado"}
    
    # Obtener notas del estudiante
    grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    avg_grade = sum(g.value for g in grades) / len(grades) if grades else 0
    
    # Obtener asistencia
    attendances = db.query(Attendance).filter(Attendance.student_id == student_id).all()
    attendance_rate = sum(1 for a in attendances if a.presence) / len(attendances) if attendances else 0
    
    # Obtener participaciones
    participations = db.query(Participation).filter(Participation.student_id == student_id).all()
    avg_participation = sum(p.score for p in participations) / len(participations) if participations else 0
    
    # Obtener predicción
    ml_service = MLService(db)
    prediction = ml_service.predict_performance(student_id)
    
    return {
        "student": {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "email": student.email
        },
        "academic_info": {
            "average_grade": avg_grade,
            "attendance_rate": attendance_rate * 100,
            "average_participation": avg_participation
        },
        "prediction": prediction if "error" not in prediction else None
    }