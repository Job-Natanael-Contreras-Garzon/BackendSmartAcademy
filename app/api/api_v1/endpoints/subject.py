from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectResponse

router = APIRouter()

@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Crear nueva materia/asignatura (solo administradores)"""
    # Verificar si ya existe una materia con el mismo nombre
    result = db.execute(
        text("SELECT id FROM subjects WHERE name = :name"),
        {"name": subject_data.name}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una materia con este nombre"
        )
    
    # Crear la materia usando SQL directo
    result = db.execute(
        text("""
        INSERT INTO subjects (name, description) 
        VALUES (:name, :description)
        RETURNING id, name, description
        """),
        {
            "name": subject_data.name,
            "description": subject_data.description
        }
    )
    
    new_subject = result.first()
    db.commit()
    
    return SubjectResponse(
        id=new_subject.id,
        name=new_subject.name,
        description=new_subject.description
    )

@router.get("/", response_model=List[SubjectResponse])
async def read_subjects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Listar materias/asignaturas"""
    result = db.execute(
        text("""
        SELECT id, name, description
        FROM subjects
        ORDER BY name
        LIMIT :limit OFFSET :skip
        """),
        {"skip": skip, "limit": limit}
    )
    
    subjects = result.fetchall()
    
    return [
        SubjectResponse(
            id=subject.id,
            name=subject.name,
            description=subject.description
        )
        for subject in subjects
    ]

@router.get("/{subject_id}", response_model=SubjectResponse)
async def read_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener materia/asignatura por ID"""
    result = db.execute(
        text("SELECT id, name, description FROM subjects WHERE id = :subject_id"),
        {"subject_id": subject_id}
    )
    
    subject = result.first()
    
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materia no encontrada"
        )
    
    return SubjectResponse(
        id=subject.id,
        name=subject.name,
        description=subject.description
    )

@router.put("/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_id: int,
    subject_data: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Actualizar materia/asignatura (solo administradores)"""
    # Verificar que la materia existe
    result = db.execute(
        text("SELECT id FROM subjects WHERE id = :subject_id"),
        {"subject_id": subject_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materia no encontrada"
        )
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"subject_id": subject_id}
    
    if subject_data.name is not None:
        # Verificar que no exista otra materia con el mismo nombre
        result = db.execute(
            text("SELECT id FROM subjects WHERE name = :name AND id != :subject_id"),
            {"name": subject_data.name, "subject_id": subject_id}
        )
        if result.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otra materia con este nombre"
            )
        
        update_fields.append("name = :name")
        params["name"] = subject_data.name
    
    if subject_data.description is not None:
        update_fields.append("description = :description")
        params["description"] = subject_data.description
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Actualizar materia usando SQL directo
    query = f"UPDATE subjects SET {', '.join(update_fields)} WHERE id = :subject_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener la materia actualizada
    result = db.execute(
        text("SELECT id, name, description FROM subjects WHERE id = :subject_id"),
        {"subject_id": subject_id}
    )
    updated_subject = result.first()
    
    return SubjectResponse(
        id=updated_subject.id,
        name=updated_subject.name,
        description=updated_subject.description
    )

@router.delete("/{subject_id}", status_code=status.HTTP_200_OK)
async def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Eliminar materia/asignatura (solo administradores)"""
    # Verificar que la materia existe
    result = db.execute(
        text("SELECT id FROM subjects WHERE id = :subject_id"),
        {"subject_id": subject_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materia no encontrada"
        )
    
    # Verificar si hay referencias a esta materia (cursos, calificaciones, etc.)
    # Aquí se podría verificar en tablas como courses u otras según el modelo de datos
    
    # Eliminar materia usando SQL directo
    db.execute(
        text("DELETE FROM subjects WHERE id = :subject_id"),
        {"subject_id": subject_id}
    )
    db.commit()
    
    return {"message": "Materia eliminada correctamente"}
