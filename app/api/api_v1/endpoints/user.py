from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user, get_password_hash
from app.models.user import User # GenderEnum and RoleEnum from model are not directly used here for response construction
from app.models.role import Role as RoleModel # For querying the roles table
from app.schemas.user import UserCreate, UserUpdate, UserResponse, GenderEnum as SchemaGenderEnum # For response construction
from app.schemas.role import RoleResponse as RoleSchemaResponse

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
    
    gender_value = user_data.gender.value # Obtener el string del enum (e.g., 'MALE', 'FEMALE', 'OTHER')
    print(f"[DEBUG CREATE_USER] gender_value for SQL will be: '{gender_value}'", flush=True)
    
    # Crear el usuario usando SQL directo para evitar problemas con enums
    from datetime import datetime
    result = db.execute(
        text("""
        INSERT INTO users (email, hashed_password, full_name, gender, role, 
                         is_active, is_superuser, phone, direction, birth_date)
        VALUES (:email, :hashed_password, :full_name, :gender, :role, 
               :is_active, :is_superuser, :phone, :direction, :birth_date)
        RETURNING id, email, full_name, phone, direction, birth_date, gender, role, is_active, is_superuser
        """),
        {
            "email": user_data.email,
            "hashed_password": get_password_hash(user_data.password),
            "full_name": user_data.full_name,
            "gender": gender_value, # Should be uppercase from user_data.gender.value
            "role": user_data.role.value, # Use .value for the string representation
            "is_active": True,
            "is_superuser": user_data.is_superuser or False,
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
    # new_user.gender es el valor string (mayúsculas) de la BD
    gender_enum = SchemaGenderEnum(new_user.gender)
    
    # Mapear rol
    # new_user.role es el valor string (mayúsculas) de la BD
    role_enum = SchemaRoleEnum(new_user.role)
    
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
    
    # RoleSchemaResponse is already imported at the top of the file
    # SchemaGenderEnum is already imported at the top of the file

    for user_row in users: # Renamed user to user_row to avoid conflict with current_user
        # Mapear género
        # user_row.gender should be 'FEMALE', 'MALE', 'OTHER' from the DB after model changes
        gender_value_from_db = user_row.gender if user_row.gender else SchemaGenderEnum.OTHER.value
        try:
            gender_enum = SchemaGenderEnum(gender_value_from_db)
        except ValueError:
            logger.warning(f"Invalid gender value '{gender_value_from_db}' for user ID {user_row.id}. Defaulting to OTHER.")
            gender_enum = SchemaGenderEnum.OTHER

        # Obtener el nombre del rol directamente de la columna user_row.role
        # Este valor debe ser 'ADMINISTRATOR', 'STUDENT', etc. (mayúsculas)
        actual_user_role_name = user_row.role

        if not actual_user_role_name:
            logger.error(f"User ID {user_row.id} has a missing or empty role in the database.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Data inconsistency: User ID {user_row.id} has no role assigned."
            )

        # Obtener y mapear rol completo desde la tabla 'roles' usando SQLAlchemy ORM
        role_model_from_db = db.query(RoleModel).filter(RoleModel.name == actual_user_role_name).first()

        role_response_obj = None
        if role_model_from_db:
            permissions_data = role_model_from_db.permissions if role_model_from_db.permissions is not None else {}
            role_response_obj = RoleSchemaResponse(
                id=role_model_from_db.id,
                name=role_model_from_db.name,
                description=role_model_from_db.description,
                permissions=permissions_data
            )
        else:
            logger.error(f"Role '{actual_user_role_name}' (from user ID {user_row.id}) not found in 'roles' table.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Data inconsistency: Role '{actual_user_role_name}' for user ID {user_row.id} not found in roles table."
            )
        
        user_responses.append(
            UserResponse(
                id=user_row.id,
                email=user_row.email,
                full_name=user_row.full_name,
                phone=user_row.phone,
                direction=user_row.direction,
                birth_date=user_row.birth_date,
                gender=gender_enum,
                role=role_response_obj, # Pass the fully constructed RoleResponse object
                photo=None,
                is_active=user_row.is_active,
                is_superuser=user_row.is_superuser
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
    print("--- ENTRANDO A update_user ---", flush=True)
    print(f"[DEBUG UPDATE_USER - ID: {user_id}] user_data recibido: {user_data.model_dump(exclude_unset=True)}", flush=True)
    """Actualizar usuario"""
    # Verificar si el usuario actual es superusuario o es el usuario a actualizar
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes para actualizar este usuario"
        )
    
    # Obtener y verificar que el usuario existe
    # Fetch all columns to log complete data
    existing_user_data_before_update_result = db.execute(
        text("SELECT * FROM users WHERE id = :user_id"), 
        {"user_id": user_id}
    )
    existing_user_data_before_update = existing_user_data_before_update_result.first()

    if not existing_user_data_before_update:
        print(f"[DEBUG UPDATE_USER - ID: {user_id}] Usuario no encontrado en la BD ANTES de la actualización.", flush=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado antes de actualizar."
        )
    
    # Convert RowProxy to dict for logging. Ensure it's not None.
    try:
        # Asegurarse de que existing_user_data_before_update no sea None antes de intentar convertirlo
        log_data_before = dict(existing_user_data_before_update._mapping) if existing_user_data_before_update else "Datos no disponibles"
    except Exception as e_dict_conv:
        print(f"[DEBUG UPDATE_USER - ID: {user_id}] Warning: Error convirtiendo RowProxy a dict para logging (antes): {str(e_dict_conv)}", flush=True)
        log_data_before = str(existing_user_data_before_update) # fallback to string representation
        
    print(f"[DEBUG UPDATE_USER - ID: {user_id}] Datos ANTES de la actualización: {log_data_before}", flush=True)
    
    # Procesar el valor de género si se proporciona
    gender_value = None
    if user_data.gender:
        gender_value = user_data.gender.value  # Obtener el valor string del enum (ej: 'MALE', 'FEMALE', 'OTHER')
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"user_id": user_id}
    
    if user_data.full_name is not None:
        update_fields.append("full_name = :full_name")
        params["full_name"] = user_data.full_name
    
    if gender_value is not None:
        update_fields.append("gender = :gender")
        params["gender"] = gender_value
        print(f"[DEBUG UPDATE_USER - ID: {{user_id}}] params['gender'] set to: '{{params['gender']}}' using gender_value: '{{gender_value}}'", flush=True)
    
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
            role_value = user_data.role.value # Obtener el valor string del enum (ej: 'STUDENT')
            update_fields.append("role = :role")
            params["role"] = role_value

        if user_data.is_superuser is not None:
            update_fields.append("is_superuser = :is_superuser")
            params["is_superuser"] = user_data.is_superuser
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Actualizar usuario usando SQL directo
    query_string = f"UPDATE users SET {', '.join(update_fields)} WHERE id = :user_id"
    print(f"[DEBUG UPDATE_USER - ID: {user_id}] Ejecutando SQL: {query_string}", flush=True)
    print(f"[DEBUG UPDATE_USER - ID: {user_id}] Con parámetros: {params}", flush=True)
    
    try:
        db.execute(text(query_string), params)
        db.commit()
        print(f"[DEBUG UPDATE_USER - ID: {user_id}] Commit realizado.", flush=True)
    except Exception as e_sql:
        db.rollback()
        print(f"[DEBUG UPDATE_USER - ID: {user_id}] Error durante SQL execute/commit: {str(e_sql)}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos durante la actualización: {str(e_sql)}"
        )
    
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
    print(f"[DEBUG UPDATE_USER - ID: {user_id}] Datos DESPUÉS de la actualización (desde BD): {dict(updated_user._mapping) if updated_user else 'No encontrado después de actualizar'}", flush=True)

    if not updated_user:
        # Esto sería muy extraño si el commit fue exitoso y no hubo error
        print(f"[DEBUG UPDATE_USER - ID: {user_id}] ¡ALERTA! El usuario no se encontró en la BD después de un commit supuestamente exitoso.", flush=True)
        # No se lanza excepción aquí para ver si el problema es que simplemente no se encuentra,
        # pero la respuesta probablemente fallará o será incorrecta.
    
    # Construir objeto UserResponse
    # Asumimos que UserResponse, SchemaGenderEnum (desde app.schemas.user) y 
    # RoleSchemaResponse (desde app.schemas.role) están importados al inicio del archivo.
    # La importación local de RoleEnum ya no es necesaria aquí.
    from app.schemas.user import GenderEnum as SchemaGenderEnum # UserResponse ya debería estar en el scope global del módulo

    # Mapear género
    gender_value_db = updated_user.gender if updated_user.gender else "other"
    gender_enum_response = None
    if gender_value_db == "female":
        gender_enum_response = SchemaGenderEnum.FEMALE
    elif gender_value_db == "male":
        gender_enum_response = SchemaGenderEnum.MALE
    else:
        gender_enum_response = SchemaGenderEnum.OTHER
    
    # Obtener el objeto Role completo para la respuesta
    role_name_to_fetch = ""
    if hasattr(updated_user, 'is_superuser') and updated_user.is_superuser:
        role_name_to_fetch = "administrator"
    else:
        role_name_to_fetch = updated_user.role if updated_user.role else "student"

    role_data_db = db.execute(
        text("SELECT id, name, description, permissions FROM roles WHERE name = :name"),
        {"name": role_name_to_fetch}
    ).first()

    role_response_obj = None
    if role_data_db:
        permissions_data = role_data_db.permissions if role_data_db.permissions is not None else {}
        role_response_obj = RoleSchemaResponse(
            id=role_data_db.id,
            name=role_data_db.name,
            description=role_data_db.description,
            permissions=permissions_data
        )
    else:
        # Fallback si el rol específico no se encuentra, intentar con 'student'
        default_role_data = db.execute(
            text("SELECT id, name, description, permissions FROM roles WHERE name = :name"),
            {"name": "student"}
        ).first()
        if default_role_data:
            permissions_data = default_role_data.permissions if default_role_data.permissions is not None else {}
            role_response_obj = RoleSchemaResponse(
                id=default_role_data.id,
                name=default_role_data.name,
                description=default_role_data.description,
                permissions=permissions_data
            )
        else: # Fallback extremo si ni 'student' existe (debería haber una mejor gestión de errores aquí)
            role_response_obj = RoleSchemaResponse(
                id=0, # ID Placeholder, idealmente esto no debería ocurrir
                name="unknown", 
                description="Role not found and default student role also not found", 
                permissions={}
            )
    
    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        full_name=updated_user.full_name,
        phone=updated_user.phone,
        direction=updated_user.direction,
        birth_date=updated_user.birth_date,
        gender=gender_enum_response,
        role=role_response_obj, # Pasar el objeto RoleSchemaResponse completo
        photo=None, 
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
    
    try:
        # Primero, eliminar las referencias del usuario en la tabla user_role
        db.execute(
            text("DELETE FROM user_role WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        
        # Luego, eliminar el usuario de la tabla users
        result = db.execute(
            text("DELETE FROM users WHERE id = :user_id RETURNING id"),
            {"user_id": user_id}
        )

        if not result.first(): # Si DELETE FROM users no devolvió filas, el usuario ya no existía (quizás eliminado en una race condition)
             # Esto podría ser redundante si la verificación anterior ya lo cubrió, pero es una doble comprobación.
             db.rollback() # Revertir la eliminación de user_role si el usuario no se eliminó de users
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado para eliminar de la tabla users, la operación fue revertida."
            )

        db.commit() # Confirmar la transacción si ambas eliminaciones fueron exitosas
    except Exception as e:
        db.rollback() # Revertir en caso de cualquier otro error durante la transacción
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el usuario: {str(e)}"
        )
    
    return {"message": f"Usuario con id {user_id} eliminado exitosamente"}
    
    return {"message": "Usuario eliminado correctamente"}