import logging
import sys
import os

# Configurar el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importamos el sistema ORM y creamos una conexión directa
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash
from app.models.user import RoleEnum
from app.core.config import settings

# Conectar directamente a la base de datos usando la configuración del proyecto
SQLALCHEMY_DATABASE_URL = settings.get_database_url()

# SQLAlchemy expects postgresql:// but many providers use postgres://
# This is a fix for that issue
if SQLALCHEMY_DATABASE_URL.startswith('postgres://'):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_admin():
    """Crea un usuario administrador directamente en la base de datos"""
    db = SessionLocal()
    try:
        # Primero, verificar qué valores de enum están permitidos en la base de datos
        logger.info("Verificando valores de enum permitidos...")
        enum_query = text("""
        SELECT enumlabel FROM pg_enum 
        JOIN pg_type ON pg_enum.enumtypid = pg_type.oid 
        WHERE pg_type.typname = 'roleenum';
        """)
        enum_result = db.execute(enum_query)
        enum_values = [row[0] for row in enum_result]
        logger.info(f"Valores de enum permitidos: {enum_values}")
        
        # Determinar el valor correcto para el administrador
        admin_role = RoleEnum.ADMINISTRATOR.value
        if admin_role not in enum_values and enum_values:
            # Intenta encontrar un valor similar
            for value in enum_values:
                if "admin" in value.lower():
                    admin_role = value
                    break
            if admin_role not in enum_values:
                # Si no se encuentra ningún valor adecuado, usa el primero disponible
                admin_role = enum_values[0] if enum_values else admin_role
        
        logger.info(f"Usando el valor de rol: {admin_role}")
        
        # Verificar si existe el usuario
        logger.info("Verificando si existe un administrador...")
        result = db.execute(text("SELECT * FROM users WHERE is_superuser = TRUE"))
        user = result.fetchone()
        
        if not user:
            logger.info("Creando usuario administrador...")
            # Crear el administrador directamente con SQL
            db.execute(
                text("""
                INSERT INTO users (email, hashed_password, full_name, is_active, is_superuser, role) 
                VALUES (:email, :password, :full_name, :is_active, :is_superuser, :role)
                """),
                {
                    "email": "admin@smartacademy.com",
                    "password": get_password_hash("admin123"),
                    "full_name": "Administrador",
                    "is_active": True,
                    "is_superuser": True,
                    "role": admin_role
                }
            )
            db.commit()
            logger.info("Usuario administrador creado exitosamente")
            logger.info("Email: admin@smartacademy.com")
            logger.info("Contraseña: admin123")
            logger.info("IMPORTANTE: Cambia esta contraseña después del primer inicio de sesión")
        else:
            logger.info("El administrador ya existe, no es necesario crearlo")
    except Exception as e:
        logger.error(f"Error al crear administrador: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Iniciando creación de administrador...")
    create_admin()
    logger.info("Proceso completado")
