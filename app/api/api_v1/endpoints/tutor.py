from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.tutor import (
    TutorStudentCreate, 
    TutorStudentUpdate, 
    TutorStudentResponse, 
    TutorStudentDetailResponse,
    RelationshipType
)

router = APIRouter()

@router.post("/", response_model=TutorStudentResponse, status_code=status.HTTP_201_CREATED)
async def assign_tutor(
    tutor_data: TutorStudentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),  # Solo administradores pueden asignar tutores
):
    """Asignar tutor a estudiante (solo administradores)"""
    # Verificar que el estudiante existe
    result = db.execute(
        text("SELECT id FROM students WHERE id = :student_id"),
        {"student_id": tutor_data.student_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar que el usuario existe
    result = db.execute(
        text("SELECT id, email FROM users WHERE id = :user_id"),
        {"user_id": tutor_data.user_id}
    )
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar que no exista ya una relación para este estudiante y usuario
    result = db.execute(
        text("""
        SELECT id 
        FROM student_tutors 
        WHERE student_id = :student_id AND user_id = :user_id
        """),
        {
            "student_id": tutor_data.student_id,
            "user_id": tutor_data.user_id
        }
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una relación tutor-estudiante con estos datos"
        )
    
    # Crear la relación tutor-estudiante
    result = db.execute(
        text("""
        INSERT INTO student_tutors (student_id, user_id, relationship, notes)
        VALUES (:student_id, :user_id, :relationship, :notes)
        RETURNING id
        """),
        {
            "student_id": tutor_data.student_id,
            "user_id": tutor_data.user_id,
            "relationship": tutor_data.relationship.value,
            "notes": tutor_data.notes
        }
    )
    tutor_id = result.first()[0]
    db.commit()
    
    # Devolver los datos de la relación creada
    return {
        "id": tutor_id,
        "student_id": tutor_data.student_id,
        "user_id": tutor_data.user_id,
        "relationship": tutor_data.relationship,
        "notes": tutor_data.notes
    }

@router.get("/student/{student_id}", response_model=List[TutorStudentDetailResponse])
async def get_student_tutors(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener tutores de un estudiante específico"""
    # Verificar que el estudiante existe
    result = db.execute(
        text("SELECT id FROM students WHERE id = :student_id"),
        {"student_id": student_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Si no es administrador, verificar si tiene permiso para ver los tutores
    if not current_user.is_superuser:
        # Si es profesor, verificar si tiene al estudiante en alguno de sus cursos
        result = db.execute(
            text("""
            SELECT c.id 
            FROM courses c
            JOIN students s ON s.group_id = c.group_id
            JOIN teachers t ON t.id = c.teacher_id
            WHERE s.id = :student_id AND t.user_id = :user_id
            """),
            {"student_id": student_id, "user_id": current_user.id}
        )
        is_teacher = result.first() is not None
        
        # Si es tutor, verificar si está asignado como tutor del estudiante
        result = db.execute(
            text("""
            SELECT id 
            FROM student_tutors 
            WHERE student_id = :student_id AND user_id = :user_id
            """),
            {"student_id": student_id, "user_id": current_user.id}
        )
        is_tutor = result.first() is not None
        
        # Si no es profesor ni tutor, verificar si es el estudiante
        result = db.execute(
            text("""
            SELECT id 
            FROM students 
            WHERE id = :student_id AND user_id = :user_id
            """),
            {"student_id": student_id, "user_id": current_user.id}
        )
        is_student = result.first() is not None
        
        if not (is_teacher or is_tutor or is_student):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver los tutores de este estudiante"
            )
    
    # Obtener todos los tutores del estudiante con detalles
    result = db.execute(
        text("""
        SELECT 
            st.id,
            st.student_id,
            st.user_id,
            st.relationship,
            st.notes,
            s.full_name as student_name,
            u.full_name as tutor_name,
            u.email as tutor_email,
            u.phone as tutor_phone
        FROM student_tutors st
        JOIN students s ON s.id = st.student_id
        JOIN users u ON u.id = st.user_id
        JOIN users su ON su.id = s.user_id
        WHERE st.student_id = :student_id
        """),
        {"student_id": student_id}
    )
    
    tutors = []
    for row in result:
        tutors.append({
            "id": row.id,
            "student_id": row.student_id,
            "user_id": row.user_id,
            "relationship": row.relationship,
            "notes": row.notes,
            "student_name": row.student_name,
            "tutor_name": row.tutor_name,
            "tutor_email": row.tutor_email,
            "tutor_phone": row.tutor_phone
        })
    
    return tutors

@router.get("/user/{user_id}", response_model=List[TutorStudentDetailResponse])
async def get_user_tutorships(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener estudiantes asociados a un tutor específico"""
    # Verificar permisos (solo el propio usuario o administradores)
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta información"
        )
    
    # Verificar que el usuario existe
    result = db.execute(
        text("SELECT id FROM users WHERE id = :user_id"),
        {"user_id": user_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Obtener todos los estudiantes asociados a este tutor
    result = db.execute(
        text("""
        SELECT 
            st.id,
            st.student_id,
            st.user_id,
            st.relationship,
            st.notes,
            s.full_name as student_name,
            u.full_name as tutor_name,
            u.email as tutor_email,
            u.phone as tutor_phone
        FROM student_tutors st
        JOIN students s ON s.id = st.student_id
        JOIN users u ON u.id = st.user_id
        JOIN users su ON su.id = s.user_id
        WHERE st.user_id = :user_id
        """),
        {"user_id": user_id}
    )
    
    students = []
    for row in result:
        students.append({
            "id": row.id,
            "student_id": row.student_id,
            "user_id": row.user_id,
            "relationship": row.relationship,
            "notes": row.notes,
            "student_name": row.student_name,
            "tutor_name": row.tutor_name,
            "tutor_email": row.tutor_email,
            "tutor_phone": row.tutor_phone
        })
    
    return students

@router.get("/{tutor_id}", response_model=TutorStudentDetailResponse)
async def get_tutor_relationship(
    tutor_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener detalle de una relación tutor-estudiante específica"""
    # Obtener la relación tutor-estudiante
    result = db.execute(
        text("""
        SELECT 
            st.id,
            st.student_id,
            st.user_id,
            st.relationship,
            st.notes,
            s.full_name as student_name,
            u.full_name as tutor_name,
            u.email as tutor_email,
            u.phone as tutor_phone,
            s.user_id as student_user_id
        FROM student_tutors st
        JOIN students s ON s.id = st.student_id
        JOIN users u ON u.id = st.user_id
        JOIN users su ON su.id = s.user_id
        WHERE st.id = :tutor_id
        """),
        {"tutor_id": tutor_id}
    )
    
    tutor = result.first()
    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación tutor-estudiante no encontrada"
        )
    
    # Verificar permisos (solo el propio tutor, el estudiante, administradores o profesores del estudiante)
    if not current_user.is_superuser and current_user.id != tutor.user_id and current_user.id != tutor.student_user_id:
        # Verificar si es profesor del estudiante
        result = db.execute(
            text("""
            SELECT c.id 
            FROM courses c
            JOIN students s ON s.group_id = c.group_id
            JOIN teachers t ON t.id = c.teacher_id
            WHERE s.id = :student_id AND t.user_id = :user_id
            """),
            {"student_id": tutor.student_id, "user_id": current_user.id}
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver esta relación tutor-estudiante"
            )
    
    return {
        "id": tutor.id,
        "student_id": tutor.student_id,
        "user_id": tutor.user_id,
        "relationship": tutor.relationship,
        "notes": tutor.notes,
        "student_name": tutor.student_name,
        "tutor_name": tutor.tutor_name,
        "tutor_email": tutor.tutor_email,
        "tutor_phone": tutor.tutor_phone
    }

@router.put("/{tutor_id}", response_model=TutorStudentResponse)
async def update_tutor_relationship(
    tutor_id: int,
    tutor_data: TutorStudentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),  # Solo administradores pueden actualizar relaciones
):
    """Actualizar relación tutor-estudiante (solo administradores)"""
    # Verificar que la relación existe
    result = db.execute(
        text("SELECT id FROM student_tutors WHERE id = :tutor_id"),
        {"tutor_id": tutor_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación tutor-estudiante no encontrada"
        )
    
    # Preparar los campos a actualizar
    update_fields = {}
    if tutor_data.relationship is not None:
        update_fields["relationship"] = tutor_data.relationship.value
    if tutor_data.notes is not None:
        update_fields["notes"] = tutor_data.notes
    
    if not update_fields:
        # No hay campos para actualizar
        result = db.execute(
            text("SELECT * FROM student_tutors WHERE id = :tutor_id"),
            {"tutor_id": tutor_id}
        )
        tutor = result.first()
        return {
            "id": tutor.id,
            "student_id": tutor.student_id,
            "user_id": tutor.user_id,
            "relationship": tutor.relationship,
            "notes": tutor.notes
        }
    
    # Construir la consulta SQL de actualización
    set_clause = ", ".join(f"{field} = :{field}" for field in update_fields)
    query = f"""
    UPDATE student_tutors 
    SET {set_clause}
    WHERE id = :tutor_id
    RETURNING id, student_id, user_id, relationship, notes
    """
    
    # Agregar el ID a los parámetros
    update_fields["tutor_id"] = tutor_id
    
    # Ejecutar la actualización
    result = db.execute(text(query), update_fields)
    updated_tutor = result.first()
    db.commit()
    
    return {
        "id": updated_tutor.id,
        "student_id": updated_tutor.student_id,
        "user_id": updated_tutor.user_id,
        "relationship": updated_tutor.relationship,
        "notes": updated_tutor.notes
    }

@router.delete("/{tutor_id}", status_code=status.HTTP_200_OK)
async def delete_tutor_relationship(
    tutor_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),  # Solo administradores pueden eliminar relaciones
):
    """Eliminar relación tutor-estudiante (solo administradores)"""
    # Verificar que la relación existe
    result = db.execute(
        text("SELECT id FROM student_tutors WHERE id = :tutor_id"),
        {"tutor_id": tutor_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación tutor-estudiante no encontrada"
        )
    
    # Eliminar la relación
    db.execute(
        text("DELETE FROM student_tutors WHERE id = :tutor_id"),
        {"tutor_id": tutor_id}
    )
    db.commit()
    
    return {"message": "Relación tutor-estudiante eliminada correctamente"}
