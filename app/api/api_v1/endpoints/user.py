from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User, GenderEnum, RoleEnum
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Crear nuevo usuario (solo administradores)"""
    # Verificar si el email ya existe
    result = db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": user_data.email}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    # Procesar el valor de género
    from app.core.security import get_password_hash
    
    gender_value = user_data.gender.lower() if user_data.gender else "other"
    if gender_value.upper() == "MALE":
        gender_value = "male"
    elif gender_value.upper() == "FEMALE":
        gender_value = "female"
    elif gender_value.upper() == "OTHER":
        gender_value = "other"
    
    # Crear el usuario usando SQL directo para evitar problemas con enums
    from datetime import datetime
    result = db.execute(
        text("""
        INSERT INTO users (email, hashed_password, full_name, gender, role, 
                         is_active, is_superuser, created_at, updated_at, phone, direction, birth_date)
        VALUES (:email, :hashed_password, :full_name, :gender, :role, 
               :is_active, :is_superuser, :created_at, :updated_at, :phone, :direction, :birth_date)
        RETURNING id, email, full_name, phone, direction, birth_date, gender, role, is_active, is_superuser
        """),
        {
            "email": user_data.email,
            "hashed_password": get_password_hash(user_data.password),
            "full_name": user_data.full_name,
            "gender": gender_value,
            "role": user_data.role,
            "is_active": True,
            "is_superuser": user_data.is_superuser or False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "phone": user_data.phone,
            "direction": user_data.direction,
            "birth_date": user_data.birth_date
        }
    )
    
    # Obtener el nuevo usuario
    new_user = result.first()
    db.commit()
    
    # Construir objeto UserResponse
    from app.schemas.user import UserResponse, GenderEnum as SchemaGenderEnum, RoleEnum as SchemaRoleEnum
    
    # Mapear género
    gender_enum = None
    if gender_value == "female":
        gender_enum = SchemaGenderEnum.FEMALE
    elif gender_value == "male":
        gender_enum = SchemaGenderEnum.MALE
    else:
        gender_enum = SchemaGenderEnum.OTHER
    
    # Mapear rol
    role_enum = None
    if new_user.role == "administrator":
        role_enum = SchemaRoleEnum.ADMINISTRATOR
    elif new_user.role == "teacher":
        role_enum = SchemaRoleEnum.TEACHER
    elif new_user.role == "parent":
        role_enum = SchemaRoleEnum.PARENT
    else:
        role_enum = SchemaRoleEnum.STUDENT
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        phone=new_user.phone,
        direction=new_user.direction,
        birth_date=new_user.birth_date,
        gender=gender_enum,
        role=role_enum,
        photo=None,
        is_active=new_user.is_active,
        is_superuser=new_user.is_superuser
    )


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Listar usuarios (solo administradores)"""
    # Obtener usuarios usando SQL directo
    result = db.execute(
        text("""
        SELECT id, email, full_name, phone, direction, birth_date, gender, role, is_active, is_superuser
        FROM users
        LIMIT :limit OFFSET :skip
        """),
        {"limit": limit, "skip": skip}
    )
    
    users = result.fetchall()
    user_responses = []
    
    # Construir objetos UserResponse
    from app.schemas.user import UserResponse, GenderEnum as SchemaGenderEnum, RoleEnum as SchemaRoleEnum
    
    for user in users:
        # Mapear género
        gender_value = user.gender if user.gender else "other"
        gender_enum = None
        if gender_value == "female":
            gender_enum = SchemaGenderEnum.FEMALE
        elif gender_value == "male":
            gender_enum = SchemaGenderEnum.MALE
        else:
            gender_enum = SchemaGenderEnum.OTHER
        
        # Mapear rol
        role_value = user.role if user.role else "student"
        role_enum = None
        if role_value == "administrator":
            role_enum = SchemaRoleEnum.ADMINISTRATOR
        elif role_value == "teacher":
            role_enum = SchemaRoleEnum.TEACHER
        elif role_value == "parent":
            role_enum = SchemaRoleEnum.PARENT
        else:
            role_enum = SchemaRoleEnum.STUDENT
        
        user_responses.append(
            UserResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                phone=user.phone,
                direction=user.direction,
                birth_date=user.birth_date,
                gender=gender_enum,
                role=role_enum,
                photo=None,
                is_active=user.is_active,
                is_superuser=user.is_superuser
            )
        )
    
    return user_responses


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener usuario por ID"""
    # Verificar si el usuario actual es superusuario o es el usuario solicitado
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes para ver este usuario"
        )
    
    # Obtener usuario usando SQL directo
    result = db.execute(
        text("""
        SELECT id, email, full_name, phone, direction, birth_date, gender, role, is_active, is_superuser
        FROM users
        WHERE id = :user_id
        """),
        {"user_id": user_id}
    )
    
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Construir objeto UserResponse
    from app.schemas.user import UserResponse, GenderEnum as SchemaGenderEnum, RoleEnum as SchemaRoleEnum
    
    # Mapear género
    gender_value = user.gender if user.gender else "other"
    gender_enum = None
    if gender_value == "female":
        gender_enum = SchemaGenderEnum.FEMALE
    elif gender_value == "male":
        gender_enum = SchemaGenderEnum.MALE
    else:
        gender_enum = SchemaGenderEnum.OTHER
    
    # Mapear rol
    role_value = user.role if user.role else "student"
    role_enum = None
    if role_value == "administrator":
        role_enum = SchemaRoleEnum.ADMINISTRATOR
    elif role_value == "teacher":
        role_enum = SchemaRoleEnum.TEACHER
    elif role_value == "parent":
        role_enum = SchemaRoleEnum.PARENT
    else:
        role_enum = SchemaRoleEnum.STUDENT
    
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        direction=user.direction,
        birth_date=user.birth_date,
        gender=gender_enum,
        role=role_enum,
        photo=None,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Actualizar usuario"""
    # Verificar si el usuario actual es superusuario o es el usuario a actualizar
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes para actualizar este usuario"
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
    
    # Procesar el valor de género si se proporciona
    gender_value = None
    if user_data.gender:
        gender_value = user_data.gender.lower()
        if gender_value.upper() == "MALE":
            gender_value = "male"
        elif gender_value.upper() == "FEMALE":
            gender_value = "female"
        elif gender_value.upper() == "OTHER":
            gender_value = "other"
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"user_id": user_id}
    
    if user_data.full_name is not None:
        update_fields.append("full_name = :full_name")
        params["full_name"] = user_data.full_name
    
    if gender_value is not None:
        update_fields.append("gender = :gender")
        params["gender"] = gender_value
    
    if user_data.phone is not None:
        update_fields.append("phone = :phone")
        params["phone"] = user_data.phone
    
    if user_data.direction is not None:
        update_fields.append("direction = :direction")
        params["direction"] = user_data.direction
    
    if user_data.birth_date is not None:
        update_fields.append("birth_date = :birth_date")
        params["birth_date"] = user_data.birth_date
    
    if user_data.photo is not None:
        update_fields.append("photo = :photo")
        params["photo"] = user_data.photo
    
    # Si es superusuario, puede actualizar campos adicionales
    if current_user.is_superuser:
        if user_data.is_active is not None:
            update_fields.append("is_active = :is_active")
            params["is_active"] = user_data.is_active
        
        if user_data.role is not None:
            # Convertir el valor del enum a string minúsculas
            role_value = user_data.role.value
            update_fields.append("role = :role")
            params["role"] = role_value
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Actualizar usuario usando SQL directo
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = :user_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener el usuario actualizado
    result = db.execute(
        text("""
        SELECT id, email, full_name, phone, direction, birth_date, gender, role, is_active, is_superuser
        FROM users
        WHERE id = :user_id
        """),
        {"user_id": user_id}
    )
    
    updated_user = result.first()
    
    # Construir objeto UserResponse
    from app.schemas.user import UserResponse, GenderEnum as SchemaGenderEnum, RoleEnum as SchemaRoleEnum
    
    # Mapear género
    gender_value = updated_user.gender if updated_user.gender else "other"
    gender_enum = None
    if gender_value == "female":
        gender_enum = SchemaGenderEnum.FEMALE
    elif gender_value == "male":
        gender_enum = SchemaGenderEnum.MALE
    else:
        gender_enum = SchemaGenderEnum.OTHER
    
    # Mapear rol
    role_value = updated_user.role if updated_user.role else "student"
    role_enum = None
    if role_value == "administrator":
        role_enum = SchemaRoleEnum.ADMINISTRATOR
    elif role_value == "teacher":
        role_enum = SchemaRoleEnum.TEACHER
    elif role_value == "parent":
        role_enum = SchemaRoleEnum.PARENT
    else:
        role_enum = SchemaRoleEnum.STUDENT
    
    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        full_name=updated_user.full_name,
        phone=updated_user.phone,
        direction=updated_user.direction,
        birth_date=updated_user.birth_date,
        gender=gender_enum,
        role=role_enum,
        photo=None,  # No devolvemos la foto para mantener liviana la respuesta
        is_active=updated_user.is_active,
        is_superuser=updated_user.is_superuser
    )


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Eliminar usuario (solo administradores)"""
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
    
    # Eliminar usuario usando SQL directo
    db.execute(
        text("DELETE FROM users WHERE id = :user_id"),
        {"user_id": user_id}
    )
    db.commit()
    
    return {"message": "Usuario eliminado correctamente"}