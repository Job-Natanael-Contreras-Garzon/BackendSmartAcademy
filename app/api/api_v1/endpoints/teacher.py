from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse, TeacherDetailResponse

router = APIRouter()

@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Crear nuevo profesor (solo administradores)"""
    # Verificar que el usuario existe
    result = db.execute(
        text("SELECT id FROM users WHERE id = :user_id"),
        {"user_id": teacher_data.user_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar que el usuario no esté ya registrado como profesor
    result = db.execute(
        text("SELECT id FROM teachers WHERE user_id = :user_id"),
        {"user_id": teacher_data.user_id}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este usuario ya está registrado como profesor"
        )
    
    # Crear el profesor usando SQL directo
    result = db.execute(
        text("""
        INSERT INTO teachers (user_id, specialization, status, teacher_code) 
        VALUES (:user_id, :specialization, :status, :teacher_code)
        RETURNING id, user_id, specialization, status, teacher_code
        """),
        {
            "user_id": teacher_data.user_id,
            "specialization": teacher_data.specialization,
            "status": teacher_data.status,
            "teacher_code": teacher_data.teacher_code
        }
    )
    
    new_teacher = result.first()
    db.commit()
    
    return TeacherResponse(
        id=new_teacher.id,
        user_id=new_teacher.user_id,
        specialization=new_teacher.specialization,
        status=new_teacher.status,
        teacher_code=new_teacher.teacher_code
    )

@router.get("/", response_model=List[TeacherDetailResponse])
async def read_teachers(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Listar profesores con opciones de filtrado"""
    # Construir la consulta base
    query = """
    SELECT t.id, t.user_id, t.specialization, t.status, t.teacher_code,
           u.full_name, u.email, u.gender, u.phone, u.photo
    FROM teachers t
    JOIN users u ON t.user_id = u.id
    WHERE 1=1
    """
    
    params = {"skip": skip, "limit": limit}
    
    # Aplicar filtro de estado si se proporciona
    if status is not None:
        query += " AND t.status = :status"
        params["status"] = status
    
    # Agregar ordenamiento y paginación
    query += " ORDER BY u.full_name LIMIT :limit OFFSET :skip"
    
    result = db.execute(text(query), params)
    teachers = result.fetchall()
    
    return [
        TeacherDetailResponse(
            id=teacher.id,
            user_id=teacher.user_id,
            specialization=teacher.specialization,
            status=teacher.status,
            teacher_code=teacher.teacher_code,
            full_name=teacher.full_name,
            email=teacher.email,
            gender=teacher.gender,
            phone=teacher.phone,
            photo=teacher.photo
        )
        for teacher in teachers
    ]

@router.get("/{teacher_id}", response_model=TeacherDetailResponse)
async def read_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener profesor por ID con detalles completos"""
    result = db.execute(
        text("""
        SELECT t.id, t.user_id, t.specialization, t.status, t.teacher_code,
               u.full_name, u.email, u.gender, u.phone, u.photo
        FROM teachers t
        JOIN users u ON t.user_id = u.id
        WHERE t.id = :teacher_id
        """),
        {"teacher_id": teacher_id}
    )
    
    teacher = result.first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )
    
    return TeacherDetailResponse(
        id=teacher.id,
        user_id=teacher.user_id,
        specialization=teacher.specialization,
        status=teacher.status,
        teacher_code=teacher.teacher_code,
        full_name=teacher.full_name,
        email=teacher.email,
        gender=teacher.gender,
        phone=teacher.phone,
        photo=teacher.photo
    )

@router.put("/{teacher_id}", response_model=TeacherResponse)
async def update_teacher(
    teacher_id: int,
    teacher_data: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Actualizar profesor (solo administradores)"""
    # Verificar que el profesor existe
    result = db.execute(
        text("SELECT id FROM teachers WHERE id = :teacher_id"),
        {"teacher_id": teacher_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"teacher_id": teacher_id}
    
    if teacher_data.specialization is not None:
        update_fields.append("specialization = :specialization")
        params["specialization"] = teacher_data.specialization
    
    if teacher_data.status is not None:
        update_fields.append("status = :status")
        params["status"] = teacher_data.status
    
    if teacher_data.teacher_code is not None:
        update_fields.append("teacher_code = :teacher_code")
        params["teacher_code"] = teacher_data.teacher_code
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Actualizar profesor usando SQL directo
    query = f"UPDATE teachers SET {', '.join(update_fields)} WHERE id = :teacher_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener el profesor actualizado
    result = db.execute(
        text("""
        SELECT id, user_id, specialization, status, teacher_code
        FROM teachers 
        WHERE id = :teacher_id
        """),
        {"teacher_id": teacher_id}
    )
    updated_teacher = result.first()
    
    return TeacherResponse(
        id=updated_teacher.id,
        user_id=updated_teacher.user_id,
        specialization=updated_teacher.specialization,
        status=updated_teacher.status,
        teacher_code=updated_teacher.teacher_code
    )

@router.delete("/{teacher_id}", status_code=status.HTTP_200_OK)
async def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Eliminar profesor (solo administradores)"""
    # Verificar que el profesor existe
    result = db.execute(
        text("SELECT id FROM teachers WHERE id = :teacher_id"),
        {"teacher_id": teacher_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )
    
    # Verificar si hay referencias a este profesor (cursos, etc.)
    result = db.execute(
        text("SELECT id FROM courses WHERE teacher_id = :teacher_id LIMIT 1"),
        {"teacher_id": teacher_id}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el profesor porque tiene cursos asignados"
        )
    
    # Eliminar profesor usando SQL directo
    db.execute(
        text("DELETE FROM teachers WHERE id = :teacher_id"),
        {"teacher_id": teacher_id}
    )
    db.commit()
    
    return {"message": "Profesor eliminado correctamente"}
