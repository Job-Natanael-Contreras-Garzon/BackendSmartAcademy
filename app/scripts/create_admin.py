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

# Conectar directamente a la base de datos usando la configuración del proyecto
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:job123@localhost:5432/SmartDB"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_admin():
    """Crea un usuario administrador directamente en la base de datos"""
    db = SessionLocal()
    try:
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
                    "role": RoleEnum.ADMINISTRATOR.value
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
