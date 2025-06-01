from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentDetailResponse

router = APIRouter()

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Crear nuevo estudiante (solo administradores)"""
    # Verificar que el usuario existe
    result = db.execute(
        text("SELECT id FROM users WHERE id = :user_id"),
        {"user_id": student_data.user_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar que el grupo existe
    if student_data.group_id:
        result = db.execute(
            text("SELECT id FROM groups WHERE id = :group_id"),
            {"group_id": student_data.group_id}
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grupo no encontrado"
            )
    
    # Verificar que el usuario no esté ya registrado como estudiante
    result = db.execute(
        text("SELECT id FROM students WHERE user_id = :user_id"),
        {"user_id": student_data.user_id}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este usuario ya está registrado como estudiante"
        )
    
    # Crear el estudiante usando SQL directo
    result = db.execute(
        text("""
        INSERT INTO students (user_id, group_id, status, student_code) 
        VALUES (:user_id, :group_id, :status, :student_code)
        RETURNING id, user_id, group_id, status, student_code
        """),
        {
            "user_id": student_data.user_id,
            "group_id": student_data.group_id,
            "status": student_data.status,
            "student_code": student_data.student_code
        }
    )
    
    new_student = result.first()
    db.commit()
    
    return StudentResponse(
        id=new_student.id,
        user_id=new_student.user_id,
        group_id=new_student.group_id,
        status=new_student.status,
        student_code=new_student.student_code
    )

@router.get("/", response_model=List[StudentDetailResponse])
async def read_students(
    skip: int = 0,
    limit: int = 100,
    group_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Listar estudiantes con opciones de filtrado"""
    # Construir la consulta base
    query = """
    SELECT s.id, s.user_id, s.group_id, s.status, s.student_code,
           u.full_name, u.email, u.gender, u.phone, u.photo,
           g.grade, g.level, g.group_name
    FROM students s
    JOIN users u ON s.user_id = u.id
    LEFT JOIN groups g ON s.group_id = g.id
    WHERE 1=1
    """
    
    params = {"skip": skip, "limit": limit}
    
    # Aplicar filtros si se proporcionan
    if group_id is not None:
        query += " AND s.group_id = :group_id"
        params["group_id"] = group_id
    
    if status is not None:
        query += " AND s.status = :status"
        params["status"] = status
    
    # Agregar ordenamiento y paginación
    query += " ORDER BY u.full_name LIMIT :limit OFFSET :skip"
    
    result = db.execute(text(query), params)
    students = result.fetchall()
    
    return [
        StudentDetailResponse(
            id=student.id,
            user_id=student.user_id,
            group_id=student.group_id,
            status=student.status,
            student_code=student.student_code,
            full_name=student.full_name,
            email=student.email,
            gender=student.gender,
            phone=student.phone,
            photo=student.photo,
            grade=student.grade,
            level=student.level,
            group_name=student.group_name
        )
        for student in students
    ]

@router.get("/{student_id}", response_model=StudentDetailResponse)
async def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener estudiante por ID con detalles completos"""
    result = db.execute(
        text("""
        SELECT s.id, s.user_id, s.group_id, s.status, s.student_code,
               u.full_name, u.email, u.gender, u.phone, u.photo,
               g.grade, g.level, g.group_name
        FROM students s
        JOIN users u ON s.user_id = u.id
        LEFT JOIN groups g ON s.group_id = g.id
        WHERE s.id = :student_id
        """),
        {"student_id": student_id}
    )
    
    student = result.first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    return StudentDetailResponse(
        id=student.id,
        user_id=student.user_id,
        group_id=student.group_id,
        status=student.status,
        student_code=student.student_code,
        full_name=student.full_name,
        email=student.email,
        gender=student.gender,
        phone=student.phone,
        photo=student.photo,
        grade=student.grade,
        level=student.level,
        group_name=student.group_name
    )

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Actualizar estudiante (solo administradores)"""
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
    
    # Verificar que el grupo existe si se proporciona
    if student_data.group_id is not None:
        result = db.execute(
            text("SELECT id FROM groups WHERE id = :group_id"),
            {"group_id": student_data.group_id}
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grupo no encontrado"
            )
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"student_id": student_id}
    
    if student_data.group_id is not None:
        update_fields.append("group_id = :group_id")
        params["group_id"] = student_data.group_id
    
    if student_data.status is not None:
        update_fields.append("status = :status")
        params["status"] = student_data.status
    
    if student_data.student_code is not None:
        update_fields.append("student_code = :student_code")
        params["student_code"] = student_data.student_code
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Actualizar estudiante usando SQL directo
    query = f"UPDATE students SET {', '.join(update_fields)} WHERE id = :student_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener el estudiante actualizado
    result = db.execute(
        text("""
        SELECT id, user_id, group_id, status, student_code
        FROM students 
        WHERE id = :student_id
        """),
        {"student_id": student_id}
    )
    updated_student = result.first()
    
    return StudentResponse(
        id=updated_student.id,
        user_id=updated_student.user_id,
        group_id=updated_student.group_id,
        status=updated_student.status,
        student_code=updated_student.student_code
    )

@router.delete("/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Eliminar estudiante (solo administradores)"""
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
    
    # Verificar si hay referencias a este estudiante (calificaciones, etc.)
    result = db.execute(
        text("SELECT id FROM grades WHERE student_id = :student_id LIMIT 1"),
        {"student_id": student_id}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el estudiante porque tiene calificaciones registradas"
        )
    
    # Eliminar estudiante usando SQL directo
    db.execute(
        text("DELETE FROM students WHERE id = :student_id"),
        {"student_id": student_id}
    )
    db.commit()
    
    return {"message": "Estudiante eliminado correctamente"}
