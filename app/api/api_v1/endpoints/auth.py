from datetime import timedelta
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password, get_current_user, get_current_active_user, get_current_active_superuser
from app.schemas.user import Token, UserCreate, UserResponse, PasswordChange, GenderEnum, RoleEnum as SchemaRoleEnum
from app.models.user import User, RoleEnum
from app.models.role import Role as RoleModel # For fetching full role details
from app.config.database import get_db

# Esquema para login con JSON
class LoginData(BaseModel):
    email: str
    password: str

# Clase para datos de registro de administrador
class AdminRegisterData(BaseModel):
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None
    direction: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[GenderEnum] = GenderEnum.OTHER

    class Config:
        from_attributes = True

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(login_data: LoginData, db: Session = Depends(get_db)):
    """Endpoint para login con formato JSON (no utiliza OAuth2)"""
    # Usar SQL crudo para evitar problemas con el Enum
    from sqlalchemy import text
    result = db.execute(
        text("SELECT * FROM users WHERE email = :email"), 
        {"email": login_data.email}
    )
    user_data = result.first()
    
    if not user_data or not verify_password(login_data.password, user_data.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    if not user_data.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )
    
    # Generar token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email, "is_superuser": user_data.is_superuser},
        expires_delta=access_token_expires
    )
    
    # Obtener el valor del rol directamente como string
    role_value = user_data.role
    if isinstance(role_value, str):
        role = role_value
    else:
        # Asignar un valor por defecto si hay problemas
        role = "student"
    
    # Devolver token con información del usuario
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user_data.id,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": role,
        "is_superuser": user_data.is_superuser
    }



@router.post("/register-admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_admin(
    admin_data: AdminRegisterData,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Registrar un nuevo administrador (solo superusuarios).
    Acepta datos en formato JSON.
    """
    # Verificar si el email ya existe (usando SQL directo para evitar problemas con los enums)
    from sqlalchemy import text
    result = db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": admin_data.email}
    )
    
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    # Procesar el género
    gender_value_for_sql = admin_data.gender.value if admin_data.gender else GenderEnum.OTHER.value
    
    # Usar SQL directo para evitar problemas con los enums
    from sqlalchemy import text
    hashed_password = get_password_hash(admin_data.password)
    # El rol para un nuevo administrador siempre será ADMINISTRATOR (en mayúsculas)
    role_value_for_sql = SchemaRoleEnum.ADMINISTRATOR.value # Esto es "ADMINISTRATOR"
    
    # Ejecutar SQL para insertar el usuario
    result = db.execute(
        text("""
        INSERT INTO users (email, hashed_password, full_name, phone, direction, 
                          birth_date, gender, role, is_active, is_superuser)
        VALUES (:email, :hashed_password, :full_name, :phone, :direction, 
                :birth_date, :gender, :role, :is_active, :is_superuser)
        RETURNING id, email, full_name, role
        """),
        {
            "email": admin_data.email,
            "hashed_password": hashed_password,
            "full_name": admin_data.full_name,
            "phone": admin_data.phone,
            "direction": admin_data.direction,
            "birth_date": admin_data.birth_date,
            "gender": gender_value_for_sql,
            "role": role_value_for_sql,
            "is_active": True,
            "is_superuser": True
        }
    )
    
    # Obtener el ID del usuario creado
    new_user = result.first()
    db.commit()
    
    # Crear un objeto usando el modelo Pydantic con los enums correctos
    from app.schemas.user import UserResponse, GenderEnum, RoleEnum as SchemaRoleEnum
    
    # Mapear el valor de género a la enumeración correspondiente
    gender_enum = None
    if gender_value == "female":
        gender_enum = GenderEnum.FEMALE
    elif gender_value == "male":
        gender_enum = GenderEnum.MALE
    else:
        gender_enum = GenderEnum.OTHER
    
    # Mapear el rol a la enumeración correspondiente
    role_enum = SchemaRoleEnum.ADMINISTRATOR
    
    # Crear el objeto UserResponse
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        phone=admin_data.phone,
        direction=admin_data.direction,
        birth_date=admin_data.birth_date,
        gender=gender_enum,
        role=role_enum,
        photo=None,
        is_active=True,
        is_superuser=True
    )

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener información del usuario actual"""
    # Import GenderEnum directly as it's not aliased like RoleEnum in the specific import line
    from app.schemas.user import GenderEnum 

    # Mapear género
    # current_user.gender is a string like 'MALE', 'FEMALE', 'OTHER'
    # GenderEnum(value) will convert the string to the Pydantic enum member
    gender_enum_for_response = GenderEnum(current_user.gender if current_user.gender else 'OTHER')

    # Obtener el nombre del rol del usuario actual (e.g., "STUDENT")
    user_role_name_str = current_user.role # This is a string like "STUDENT"

    # Buscar el objeto Role completo en la base de datos usando el nombre del rol
    role_db_object = db.query(RoleModel).filter(RoleModel.name == user_role_name_str).first()

    if not role_db_object:
        # This shouldn't happen if data is consistent (user has a role that exists in roles table)
        # Consider how to handle this: raise error, or default role, or make role Optional in UserResponse
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Role '{user_role_name_str}' assigned to user but not found in roles table."
        )

    # Crear el objeto UserResponse
    # Pydantic will use role_db_object (a RoleModel instance)
    # and convert it to RoleSchemaResponse (defined in UserResponse.role) due to `from_attributes = True`
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        direction=current_user.direction,
        birth_date=current_user.birth_date,
        gender=gender_enum_for_response, # Pass the Pydantic GenderEnum member
        role=role_db_object,  # Pass the full RoleModel SQLAlchemy object
        photo=current_user.photo,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser
    )

@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: PasswordChange,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cambiar contraseña del usuario actual"""
    # Verificar la contraseña actual
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    # Generar el hash de la nueva contraseña
    hashed_password = get_password_hash(password_data.new_password)
    
    # Actualizar la contraseña usando SQL directo
    from sqlalchemy import text
    db.execute(
        text("UPDATE users SET hashed_password = :hashed_password WHERE id = :user_id"),
        {"hashed_password": hashed_password, "user_id": current_user.id}
    )
    db.commit()
    
    return {"message": "Contraseña actualizada correctamente"}