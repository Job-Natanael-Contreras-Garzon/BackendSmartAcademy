from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate, RoleAssignment

router = APIRouter()

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    *,
    db: Session = Depends(get_db),
    role_in: RoleCreate,
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Crear un nuevo rol (solo administradores).
    """
    # Verificar si el nombre de rol ya existe
    role = db.query(Role).filter(Role.name == role_in.name).first()
    if role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un rol con este nombre"
        )
    
    # Crear el rol
    role = Role(
        name=role_in.name,
        description=role_in.description,
        permissions=role_in.permissions
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.get("/", response_model=List[RoleResponse])
async def read_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),  # Solo administradores
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Recuperar roles (solo administradores).
    """
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles

@router.get("/{role_id}", response_model=RoleResponse)
async def read_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: User = Depends(get_current_active_superuser)  # Solo administradores
) -> Any:
    """
    Obtener un rol específico por ID (solo administradores).
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return role

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    role_in: RoleUpdate,
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Actualizar un rol (solo administradores).
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    # Actualizar campos
    update_data = role_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(role, field, value)
    
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: User = Depends(get_current_active_superuser)
) -> None:
    """
    Eliminar un rol (solo administradores).
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    db.delete(role)
    db.commit()

@router.post("/assign/{user_id}", status_code=status.HTTP_200_OK)
async def assign_role_to_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    role_assignment: RoleAssignment,
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Asignar un rol a un usuario (solo administradores).
    """
    # Verificar si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar si el rol existe
    role = db.query(Role).filter(Role.id == role_assignment.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    # Asignar rol al usuario
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
    
    return {"message": f"Rol '{role.name}' asignado correctamente al usuario"}

@router.get("/user/{user_id}", response_model=List[RoleResponse])
async def get_user_roles(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: User = Depends(get_current_active_superuser)  # Solo administradores
) -> Any:
    """
    Obtener todos los roles asignados a un usuario (solo administradores).
    """
    # Verificar si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user.roles
