from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user, get_current_active_teacher
from app.models.user import User
from app.schemas.grade import GradeCreate, GradeUpdate, GradeResponse, GradeDetailResponse

router = APIRouter()

@router.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
async def create_grade(
    grade_data: GradeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_teacher),  # Solo profesores pueden crear calificaciones
):
    """Crear nueva calificación (solo profesores)"""
    # Verificar que el estudiante existe
    result = db.execute(
        text("SELECT id FROM students WHERE id = :student_id"),
        {"student_id": grade_data.student_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar que el curso existe
    result = db.execute(
        text("SELECT id FROM courses WHERE id = :course_id"),
        {"course_id": grade_data.course_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar que el profesor tiene permiso para calificar este curso
    # (debe ser el profesor asignado al curso)
    result = db.execute(
        text("""
        SELECT c.id 
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        WHERE c.id = :course_id AND t.user_id = :user_id
        """),
        {"course_id": grade_data.course_id, "user_id": current_user.id}
    )
    if not result.first() and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para calificar este curso"
        )
    
    # Verificar que el estudiante está en el curso (a través del grupo asignado al curso)
    result = db.execute(
        text("""
        SELECT s.id 
        FROM students s
        JOIN courses c ON s.group_id = c.group_id
        WHERE s.id = :student_id AND c.id = :course_id
        """),
        {"student_id": grade_data.student_id, "course_id": grade_data.course_id}
    )
    if not result.first():
        # Si no hay coincidencia por grupo, advertir pero permitir (podría ser un caso especial)
        print("Advertencia: El estudiante no está en el grupo asignado a este curso")
    
    # Establecer fecha de registro si no se proporciona
    date_recorded = grade_data.date_recorded or date.today()
    
    # Crear la calificación usando SQL directo
    result = db.execute(
        text("""
        INSERT INTO grades (student_id, course_id, period, value, date_recorded) 
        VALUES (:student_id, :course_id, :period, :value, :date_recorded)
        RETURNING id, student_id, course_id, period, value, date_recorded
        """),
        {
            "student_id": grade_data.student_id,
            "course_id": grade_data.course_id,
            "period": grade_data.period,
            "value": grade_data.value,
            "date_recorded": date_recorded
        }
    )
    
    new_grade = result.first()
    db.commit()
    
    return GradeResponse(
        id=new_grade.id,
        student_id=new_grade.student_id,
        course_id=new_grade.course_id,
        period=new_grade.period,
        value=new_grade.value,
        date_recorded=new_grade.date_recorded
    )

@router.get("/", response_model=List[GradeDetailResponse])
async def read_grades(
    skip: int = 0,
    limit: int = 100,
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    period: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Listar calificaciones con opciones de filtrado"""
    # Construir la consulta base
    query = """
    SELECT g.id, g.student_id, g.course_id, g.period, g.value, g.date_recorded,
           CONCAT(u.full_name) as student_name, s.student_code,
           sb.name as subject_name, 
           tu.full_name as teacher_name,
           gr.group_name
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN users u ON s.user_id = u.id
    JOIN courses c ON g.course_id = c.id
    JOIN subjects sb ON c.subject_id = sb.id
    JOIN teachers t ON c.teacher_id = t.id
    JOIN users tu ON t.user_id = tu.id
    LEFT JOIN groups gr ON s.group_id = gr.id
    WHERE 1=1
    """
    
    params = {"skip": skip, "limit": limit}
    
    # Aplicar filtros si se proporcionan
    if student_id is not None:
        query += " AND g.student_id = :student_id"
        params["student_id"] = student_id
    
    if course_id is not None:
        query += " AND g.course_id = :course_id"
        params["course_id"] = course_id
    
    if period is not None:
        query += " AND g.period = :period"
        params["period"] = period
    
    # Aplicar filtros basados en el rol del usuario
    if not current_user.is_superuser:
        # Si es profesor, solo ve calificaciones de sus cursos
        result = db.execute(
            text("SELECT id FROM teachers WHERE user_id = :user_id"),
            {"user_id": current_user.id}
        )
        teacher = result.first()
        
        if teacher:
            query += " AND c.teacher_id = :teacher_id"
            params["teacher_id"] = teacher.id
        else:
            # Si es estudiante, solo ve sus propias calificaciones
            result = db.execute(
                text("SELECT id FROM students WHERE user_id = :user_id"),
                {"user_id": current_user.id}
            )
            student = result.first()
            
            if student:
                query += " AND g.student_id = :student_id"
                params["student_id"] = student.id
            else:
                # Si no es profesor ni estudiante, no debería ver calificaciones
                return []
    
    # Agregar ordenamiento y paginación
    query += " ORDER BY g.date_recorded DESC, u.full_name LIMIT :limit OFFSET :skip"
    
    result = db.execute(text(query), params)
    grades = result.fetchall()
    
    return [
        GradeDetailResponse(
            id=grade.id,
            student_id=grade.student_id,
            course_id=grade.course_id,
            period=grade.period,
            value=grade.value,
            date_recorded=grade.date_recorded,
            student_name=grade.student_name,
            student_code=grade.student_code,
            subject_name=grade.subject_name,
            teacher_name=grade.teacher_name,
            group_name=grade.group_name
        )
        for grade in grades
    ]

@router.get("/{grade_id}", response_model=GradeDetailResponse)
async def read_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener calificación por ID con detalles completos"""
    # Verificar permisos (solo administradores, profesor del curso o el propio estudiante)
    if not current_user.is_superuser:
        # Verificar si es profesor del curso
        result = db.execute(
            text("""
            SELECT g.id 
            FROM grades g
            JOIN courses c ON g.course_id = c.id
            JOIN teachers t ON c.teacher_id = t.id
            WHERE g.id = :grade_id AND t.user_id = :user_id
            """),
            {"grade_id": grade_id, "user_id": current_user.id}
        )
        is_teacher = result.first() is not None
        
        # Verificar si es el estudiante
        result = db.execute(
            text("""
            SELECT g.id 
            FROM grades g
            JOIN students s ON g.student_id = s.id
            WHERE g.id = :grade_id AND s.user_id = :user_id
            """),
            {"grade_id": grade_id, "user_id": current_user.id}
        )
        is_student = result.first() is not None
        
        if not (is_teacher or is_student):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver esta calificación"
            )
    
    # Obtener la calificación con todos sus detalles
    result = db.execute(
        text("""
        SELECT g.id, g.student_id, g.course_id, g.period, g.value, g.date_recorded,
               CONCAT(u.full_name) as student_name, s.student_code,
               sb.name as subject_name, 
               tu.full_name as teacher_name,
               gr.group_name
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN users u ON s.user_id = u.id
        JOIN courses c ON g.course_id = c.id
        JOIN subjects sb ON c.subject_id = sb.id
        JOIN teachers t ON c.teacher_id = t.id
        JOIN users tu ON t.user_id = tu.id
        LEFT JOIN groups gr ON s.group_id = gr.id
        WHERE g.id = :grade_id
        """),
        {"grade_id": grade_id}
    )
    
    grade = result.first()
    
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada"
        )
    
    return GradeDetailResponse(
        id=grade.id,
        student_id=grade.student_id,
        course_id=grade.course_id,
        period=grade.period,
        value=grade.value,
        date_recorded=grade.date_recorded,
        student_name=grade.student_name,
        student_code=grade.student_code,
        subject_name=grade.subject_name,
        teacher_name=grade.teacher_name,
        group_name=grade.group_name
    )

@router.put("/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int,
    grade_data: GradeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_teacher),  # Solo profesores pueden actualizar calificaciones
):
    """Actualizar calificación (solo profesores)"""
    # Verificar que la calificación existe
    result = db.execute(
        text("SELECT id, course_id FROM grades WHERE id = :grade_id"),
        {"grade_id": grade_id}
    )
    grade = result.first()
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada"
        )
    
    # Verificar que el profesor tiene permiso para modificar esta calificación
    # (debe ser el profesor asignado al curso)
    result = db.execute(
        text("""
        SELECT c.id 
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        WHERE c.id = :course_id AND t.user_id = :user_id
        """),
        {"course_id": grade.course_id, "user_id": current_user.id}
    )
    if not result.first() and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta calificación"
        )
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"grade_id": grade_id}
    
    if grade_data.value is not None:
        update_fields.append("value = :value")
        params["value"] = grade_data.value
    
    if grade_data.period is not None:
        update_fields.append("period = :period")
        params["period"] = grade_data.period
    
    if grade_data.date_recorded is not None:
        update_fields.append("date_recorded = :date_recorded")
        params["date_recorded"] = grade_data.date_recorded
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Actualizar calificación usando SQL directo
    query = f"UPDATE grades SET {', '.join(update_fields)} WHERE id = :grade_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener la calificación actualizada
    result = db.execute(
        text("""
        SELECT id, student_id, course_id, period, value, date_recorded
        FROM grades 
        WHERE id = :grade_id
        """),
        {"grade_id": grade_id}
    )
    updated_grade = result.first()
    
    return GradeResponse(
        id=updated_grade.id,
        student_id=updated_grade.student_id,
        course_id=updated_grade.course_id,
        period=updated_grade.period,
        value=updated_grade.value,
        date_recorded=updated_grade.date_recorded
    )

@router.delete("/{grade_id}", status_code=status.HTTP_200_OK)
async def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_teacher),  # Solo profesores pueden eliminar calificaciones
):
    """Eliminar calificación (solo profesores)"""
    # Verificar que la calificación existe
    result = db.execute(
        text("SELECT id, course_id FROM grades WHERE id = :grade_id"),
        {"grade_id": grade_id}
    )
    grade = result.first()
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada"
        )
    
    # Verificar que el profesor tiene permiso para eliminar esta calificación
    # (debe ser el profesor asignado al curso)
    result = db.execute(
        text("""
        SELECT c.id 
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        WHERE c.id = :course_id AND t.user_id = :user_id
        """),
        {"course_id": grade.course_id, "user_id": current_user.id}
    )
    if not result.first() and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta calificación"
        )
    
    # Eliminar calificación usando SQL directo
    db.execute(
        text("DELETE FROM grades WHERE id = :grade_id"),
        {"grade_id": grade_id}
    )
    db.commit()
    
    return {"message": "Calificación eliminada correctamente"}