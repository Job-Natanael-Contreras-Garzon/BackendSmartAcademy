from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User, RoleEnum
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse

router = APIRouter()

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Crear nuevo rol (solo administradores)"""
    # Verificar si el nombre del rol ya existe
    result = db.execute(
        text("SELECT id FROM roles WHERE name = :name"),
        {"name": role_data.name}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre del rol ya está registrado"
        )
    
    # Crear el rol usando SQL directo
    from datetime import datetime
    result = db.execute(
        text("""
        INSERT INTO roles (name, description, permissions, created_at, updated_at)
        VALUES (:name, :description, :permissions, :created_at, :updated_at)
        RETURNING id, name, description, permissions
        """),
        {
            "name": role_data.name,
            "description": role_data.description,
            "permissions": role_data.permissions,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    )
    
    # Obtener el nuevo rol
    new_role = result.first()
    db.commit()
    
    return RoleResponse(
        id=new_role.id,
        name=new_role.name,
        description=new_role.description,
        permissions=new_role.permissions,
    )

@router.get("/", response_model=List[RoleResponse])
async def read_roles(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Listar roles"""
    result = db.execute(
        text("SELECT id, name, description, permissions FROM roles")
    )
    roles = result.fetchall()
    
    return [
        RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=role.permissions,
        )
        for role in roles
    ]

@router.get("/{role_id}", response_model=RoleResponse)
async def read_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener rol por ID"""
    result = db.execute(
        text("SELECT id, name, description, permissions FROM roles WHERE id = :role_id"),
        {"role_id": role_id}
    )
    role = result.first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    return RoleResponse(
        id=role.id,
        name=role.name,
        description=role.description,
        permissions=role.permissions,
    )

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Actualizar rol (solo administradores)"""
    # Verificar que el rol existe
    result = db.execute(
        text("SELECT id FROM roles WHERE id = :role_id"),
        {"role_id": role_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"role_id": role_id}
    
    if role_data.name is not None:
        # Verificar que el nombre no exista ya para otro rol
        result = db.execute(
            text("SELECT id FROM roles WHERE name = :name AND id != :role_id"),
            {"name": role_data.name, "role_id": role_id}
        )
        if result.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del rol ya está registrado para otro rol"
            )
        update_fields.append("name = :name")
        params["name"] = role_data.name
    
    if role_data.description is not None:
        update_fields.append("description = :description")
        params["description"] = role_data.description
    
    if role_data.permissions is not None:
        update_fields.append("permissions = :permissions")
        params["permissions"] = role_data.permissions
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Actualizar rol usando SQL directo
    from datetime import datetime
    params["updated_at"] = datetime.now()
    update_fields.append("updated_at = :updated_at")
    
    query = f"UPDATE roles SET {', '.join(update_fields)} WHERE id = :role_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener el rol actualizado
    result = db.execute(
        text("SELECT id, name, description, permissions FROM roles WHERE id = :role_id"),
        {"role_id": role_id}
    )
    updated_role = result.first()
    
    return RoleResponse(
        id=updated_role.id,
        name=updated_role.name,
        description=updated_role.description,
        permissions=updated_role.permissions,
    )

@router.delete("/{role_id}", status_code=status.HTTP_200_OK)
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Eliminar rol (solo administradores)"""
    # Verificar que el rol existe
    result = db.execute(
        text("SELECT id FROM roles WHERE id = :role_id"),
        {"role_id": role_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    # Verificar si hay usuarios que tengan este rol
    result = db.execute(
        text("SELECT id FROM users WHERE role_id = :role_id"),
        {"role_id": role_id}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el rol porque está asignado a usuarios"
        )
    
    # Eliminar rol usando SQL directo
    db.execute(
        text("DELETE FROM roles WHERE id = :role_id"),
        {"role_id": role_id}
    )
    db.commit()
    
    return {"message": "Rol eliminado correctamente"}

@router.post("/assign/{user_id}", status_code=status.HTTP_200_OK)
async def assign_role_to_user(
    user_id: int,
    role_id: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Asignar rol a usuario (solo administradores)"""
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
    
    # Verificar que el rol existe
    result = db.execute(
        text("SELECT id, name FROM roles WHERE id = :role_id"),
        {"role_id": role_id}
    )
    role = result.first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    # Asignar rol al usuario usando SQL directo
    db.execute(
        text("UPDATE users SET role = :role_name WHERE id = :user_id"),
        {"role_name": role.name, "user_id": user_id}
    )
    db.commit()
    
    return {"message": f"Rol '{role.name}' asignado al usuario correctamente"}

@router.get("/user/{user_id}", response_model=RoleResponse)
async def get_user_role(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener rol de un usuario"""
    # Verificar si el usuario actual es superusuario o es el usuario solicitado
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes para ver este rol"
        )
    
    # Obtener el rol del usuario
    result = db.execute(
        text("""
        SELECT r.id, r.name, r.description, r.permissions
        FROM users u
        JOIN roles r ON u.role = r.name
        WHERE u.id = :user_id
        """),
        {"user_id": user_id}
    )
    role = result.first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario o rol no encontrado"
        )
    
    return RoleResponse(
        id=role.id,
        name=role.name,
        description=role.description,
        permissions=role.permissions,
    )
