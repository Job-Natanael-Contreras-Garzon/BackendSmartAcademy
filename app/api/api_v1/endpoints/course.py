from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse, CourseDetailResponse

router = APIRouter()

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Crear nuevo curso (solo administradores)"""
    # Verificar que el profesor existe
    result = db.execute(
        text("SELECT id FROM teachers WHERE id = :teacher_id"),
        {"teacher_id": course_data.teacher_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )
    
    # Verificar que la materia existe
    result = db.execute(
        text("SELECT id FROM subjects WHERE id = :subject_id"),
        {"subject_id": course_data.subject_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materia no encontrada"
        )
    
    # Verificar que el grupo existe si se proporciona
    if course_data.group_id is not None:
        result = db.execute(
            text("SELECT id FROM groups WHERE id = :group_id"),
            {"group_id": course_data.group_id}
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grupo no encontrado"
            )
    
    # Verificar que el periodo existe si se proporciona
    if course_data.period_id is not None:
        result = db.execute(
            text("SELECT id FROM periods WHERE id = :period_id"),
            {"period_id": course_data.period_id}
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periodo no encontrado"
            )
    
    # Verificar que no exista una combinación idéntica
    if course_data.group_id and course_data.period_id:
        result = db.execute(
            text("""
            SELECT id FROM courses 
            WHERE teacher_id = :teacher_id AND subject_id = :subject_id 
            AND group_id = :group_id AND period_id = :period_id
            """),
            {
                "teacher_id": course_data.teacher_id,
                "subject_id": course_data.subject_id,
                "group_id": course_data.group_id,
                "period_id": course_data.period_id
            }
        )
        if result.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un curso con esa combinación de profesor, materia, grupo y periodo"
            )
    
    # Crear el curso usando SQL directo
    result = db.execute(
        text("""
        INSERT INTO courses (teacher_id, subject_id, group_id, period_id, description) 
        VALUES (:teacher_id, :subject_id, :group_id, :period_id, :description)
        RETURNING id, teacher_id, subject_id, group_id, period_id, description
        """),
        {
            "teacher_id": course_data.teacher_id,
            "subject_id": course_data.subject_id,
            "group_id": course_data.group_id,
            "period_id": course_data.period_id,
            "description": course_data.description
        }
    )
    
    new_course = result.first()
    db.commit()
    
    return CourseResponse(
        id=new_course.id,
        teacher_id=new_course.teacher_id,
        subject_id=new_course.subject_id,
        group_id=new_course.group_id,
        period_id=new_course.period_id,
        description=new_course.description
    )

@router.get("/", response_model=List[CourseDetailResponse])
async def read_courses(
    skip: int = 0,
    limit: int = 100,
    teacher_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    group_id: Optional[int] = None,
    period_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Listar cursos con opciones de filtrado"""
    # Construir la consulta base
    query = """
    SELECT c.id, c.teacher_id, c.subject_id, c.group_id, c.period_id, c.description,
           u.full_name as teacher_name, s.name as subject_name,
           g.group_name, g.grade, g.level,
           p.name as period_name
    FROM courses c
    JOIN teachers t ON c.teacher_id = t.id
    JOIN users u ON t.user_id = u.id
    JOIN subjects s ON c.subject_id = s.id
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN periods p ON c.period_id = p.id
    WHERE 1=1
    """
    
    params = {"skip": skip, "limit": limit}
    
    # Aplicar filtros si se proporcionan
    if teacher_id is not None:
        query += " AND c.teacher_id = :teacher_id"
        params["teacher_id"] = teacher_id
    
    if subject_id is not None:
        query += " AND c.subject_id = :subject_id"
        params["subject_id"] = subject_id
    
    if group_id is not None:
        query += " AND c.group_id = :group_id"
        params["group_id"] = group_id
    
    if period_id is not None:
        query += " AND c.period_id = :period_id"
        params["period_id"] = period_id
    
    # Agregar ordenamiento y paginación
    query += " ORDER BY s.name, u.full_name LIMIT :limit OFFSET :skip"
    
    result = db.execute(text(query), params)
    courses = result.fetchall()
    
    return [
        CourseDetailResponse(
            id=course.id,
            teacher_id=course.teacher_id,
            subject_id=course.subject_id,
            group_id=course.group_id,
            period_id=course.period_id,
            description=course.description,
            teacher_name=course.teacher_name,
            subject_name=course.subject_name,
            group_name=course.group_name,
            grade=course.grade,
            level=course.level,
            period_name=course.period_name
        )
        for course in courses
    ]

@router.get("/{course_id}", response_model=CourseDetailResponse)
async def read_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener curso por ID con detalles completos"""
    result = db.execute(
        text("""
        SELECT c.id, c.teacher_id, c.subject_id, c.group_id, c.period_id, c.description,
               u.full_name as teacher_name, s.name as subject_name,
               g.group_name, g.grade, g.level,
               p.name as period_name
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        JOIN users u ON t.user_id = u.id
        JOIN subjects s ON c.subject_id = s.id
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN periods p ON c.period_id = p.id
        WHERE c.id = :course_id
        """),
        {"course_id": course_id}
    )
    
    course = result.first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    return CourseDetailResponse(
        id=course.id,
        teacher_id=course.teacher_id,
        subject_id=course.subject_id,
        group_id=course.group_id,
        period_id=course.period_id,
        description=course.description,
        teacher_name=course.teacher_name,
        subject_name=course.subject_name,
        group_name=course.group_name,
        grade=course.grade,
        level=course.level,
        period_name=course.period_name
    )

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Actualizar curso (solo administradores)"""
    # Verificar que el curso existe
    result = db.execute(
        text("SELECT id FROM courses WHERE id = :course_id"),
        {"course_id": course_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar relaciones si se proporcionan valores
    if course_data.teacher_id is not None:
        result = db.execute(
            text("SELECT id FROM teachers WHERE id = :teacher_id"),
            {"teacher_id": course_data.teacher_id}
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesor no encontrado"
            )
    
    if course_data.subject_id is not None:
        result = db.execute(
            text("SELECT id FROM subjects WHERE id = :subject_id"),
            {"subject_id": course_data.subject_id}
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Materia no encontrada"
            )
    
    if course_data.group_id is not None:
        result = db.execute(
            text("SELECT id FROM groups WHERE id = :group_id"),
            {"group_id": course_data.group_id}
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grupo no encontrado"
            )
    
    if course_data.period_id is not None:
        result = db.execute(
            text("SELECT id FROM periods WHERE id = :period_id"),
            {"period_id": course_data.period_id}
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periodo no encontrado"
            )
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"course_id": course_id}
    
    if course_data.teacher_id is not None:
        update_fields.append("teacher_id = :teacher_id")
        params["teacher_id"] = course_data.teacher_id
    
    if course_data.subject_id is not None:
        update_fields.append("subject_id = :subject_id")
        params["subject_id"] = course_data.subject_id
    
    if course_data.group_id is not None:
        update_fields.append("group_id = :group_id")
        params["group_id"] = course_data.group_id
    
    if course_data.period_id is not None:
        update_fields.append("period_id = :period_id")
        params["period_id"] = course_data.period_id
    
    if course_data.description is not None:
        update_fields.append("description = :description")
        params["description"] = course_data.description
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Verificar duplicados si se actualizan campos clave
    if any(field in ["teacher_id", "subject_id", "group_id", "period_id"] for field in params.keys() if field != "course_id"):
        # Obtener valores actuales para campos que no se actualizan
        current_course = db.execute(
            text("SELECT teacher_id, subject_id, group_id, period_id FROM courses WHERE id = :course_id"),
            {"course_id": course_id}
        ).first()
        
        # Completar params con valores actuales para la verificación
        if "teacher_id" not in params:
            params["teacher_id"] = current_course.teacher_id
        if "subject_id" not in params:
            params["subject_id"] = current_course.subject_id
        if "group_id" not in params:
            params["group_id"] = current_course.group_id
        if "period_id" not in params:
            params["period_id"] = current_course.period_id
        
        # Verificar que no exista otro curso con la misma combinación
        result = db.execute(
            text("""
            SELECT id FROM courses 
            WHERE teacher_id = :teacher_id AND subject_id = :subject_id 
            AND group_id = :group_id AND period_id = :period_id
            AND id != :course_id
            """),
            params
        )
        if result.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro curso con esa combinación de profesor, materia, grupo y periodo"
            )
    
    # Actualizar curso usando SQL directo
    query = f"UPDATE courses SET {', '.join(update_fields)} WHERE id = :course_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener el curso actualizado
    result = db.execute(
        text("""
        SELECT id, teacher_id, subject_id, group_id, period_id, description
        FROM courses 
        WHERE id = :course_id
        """),
        {"course_id": course_id}
    )
    updated_course = result.first()
    
    return CourseResponse(
        id=updated_course.id,
        teacher_id=updated_course.teacher_id,
        subject_id=updated_course.subject_id,
        group_id=updated_course.group_id,
        period_id=updated_course.period_id,
        description=updated_course.description
    )

@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Eliminar curso (solo administradores)"""
    # Verificar que el curso existe
    result = db.execute(
        text("SELECT id FROM courses WHERE id = :course_id"),
        {"course_id": course_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar si hay calificaciones asociadas a este curso
    result = db.execute(
        text("SELECT id FROM grades WHERE course_id = :course_id LIMIT 1"),
        {"course_id": course_id}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el curso porque tiene calificaciones registradas"
        )
    
    # Eliminar curso usando SQL directo
    db.execute(
        text("DELETE FROM courses WHERE id = :course_id"),
        {"course_id": course_id}
    )
    db.commit()
    
    return {"message": "Curso eliminado correctamente"}
