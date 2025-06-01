from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.group import GroupCreate, GroupUpdate, GroupResponse

router = APIRouter()

@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: GroupCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Crear nuevo grupo académico (solo administradores)"""
    # Verificar si ya existe un grupo con el mismo nombre y nivel
    result = db.execute(
        text("""
        SELECT id FROM groups 
        WHERE grade = :grade AND level = :level AND group_name = :group_name
        """),
        {
            "grade": group_data.grade,
            "level": group_data.level,
            "group_name": group_data.group_name
        }
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un grupo con el mismo grado, nivel y nombre"
        )
    
    # Crear el grupo usando SQL directo
    result = db.execute(
        text("""
        INSERT INTO groups (grade, level, group_name) 
        VALUES (:grade, :level, :group_name)
        RETURNING id, grade, level, group_name
        """),
        {
            "grade": group_data.grade,
            "level": group_data.level,
            "group_name": group_data.group_name
        }
    )
    
    new_group = result.first()
    db.commit()
    
    return GroupResponse(
        id=new_group.id,
        grade=new_group.grade,
        level=new_group.level,
        group_name=new_group.group_name
    )

@router.get("/", response_model=List[GroupResponse])
async def read_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Listar grupos académicos"""
    result = db.execute(
        text("""
        SELECT id, grade, level, group_name
        FROM groups
        ORDER BY grade, level, group_name
        LIMIT :limit OFFSET :skip
        """),
        {"skip": skip, "limit": limit}
    )
    
    groups = result.fetchall()
    
    return [
        GroupResponse(
            id=group.id,
            grade=group.grade,
            level=group.level,
            group_name=group.group_name
        )
        for group in groups
    ]

@router.get("/{group_id}", response_model=GroupResponse)
async def read_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener grupo académico por ID"""
    result = db.execute(
        text("SELECT id, grade, level, group_name FROM groups WHERE id = :group_id"),
        {"group_id": group_id}
    )
    
    group = result.first()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado"
        )
    
    return GroupResponse(
        id=group.id,
        grade=group.grade,
        level=group.level,
        group_name=group.group_name
    )

@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: int,
    group_data: GroupUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Actualizar grupo académico (solo administradores)"""
    # Verificar que el grupo existe
    result = db.execute(
        text("SELECT id FROM groups WHERE id = :group_id"),
        {"group_id": group_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado"
        )
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"group_id": group_id}
    
    if group_data.grade is not None:
        update_fields.append("grade = :grade")
        params["grade"] = group_data.grade
    
    if group_data.level is not None:
        update_fields.append("level = :level")
        params["level"] = group_data.level
    
    if group_data.group_name is not None:
        update_fields.append("group_name = :group_name")
        params["group_name"] = group_data.group_name
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Verificar si el grupo actualizado no duplica otro existente
    if len(update_fields) > 0:
        # Obtenemos los valores actuales para los campos que no se actualizan
        current_group = db.execute(
            text("SELECT grade, level, group_name FROM groups WHERE id = :group_id"),
            {"group_id": group_id}
        ).first()
        
        # Completamos los params con los valores actuales para los campos que no se actualizan
        if "grade" not in params:
            params["grade"] = current_group.grade
        if "level" not in params:
            params["level"] = current_group.level
        if "group_name" not in params:
            params["group_name"] = current_group.group_name
        
        # Verificamos que no exista otro grupo con los mismos valores
        duplicate = db.execute(
            text("""
            SELECT id FROM groups 
            WHERE grade = :grade AND level = :level AND group_name = :group_name AND id != :group_id
            """),
            params
        ).first()
        
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro grupo con esas características"
            )
    
    # Actualizar grupo usando SQL directo
    query = f"UPDATE groups SET {', '.join(update_fields)} WHERE id = :group_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener el grupo actualizado
    result = db.execute(
        text("SELECT id, grade, level, group_name FROM groups WHERE id = :group_id"),
        {"group_id": group_id}
    )
    updated_group = result.first()
    
    return GroupResponse(
        id=updated_group.id,
        grade=updated_group.grade,
        level=updated_group.level,
        group_name=updated_group.group_name
    )

@router.delete("/{group_id}", status_code=status.HTTP_200_OK)
async def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Eliminar grupo académico (solo administradores)"""
    # Verificar que el grupo existe
    result = db.execute(
        text("SELECT id FROM groups WHERE id = :group_id"),
        {"group_id": group_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado"
        )
    
    # Verificar si hay estudiantes asignados a este grupo
    result = db.execute(
        text("SELECT id FROM students WHERE group_id = :group_id LIMIT 1"),
        {"group_id": group_id}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el grupo porque tiene estudiantes asignados"
        )
    
    # Eliminar grupo usando SQL directo
    db.execute(
        text("DELETE FROM groups WHERE id = :group_id"),
        {"group_id": group_id}
    )
    db.commit()
    
    return {"message": "Grupo eliminado correctamente"}
