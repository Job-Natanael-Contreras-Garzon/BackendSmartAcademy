import logging
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, RoleEnum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    db = SessionLocal()
    try:
        # Verificar si ya existe un usuario administrador
        user = db.query(User).filter(User.is_superuser == True).first()
        if not user:
            logger.info("Creando usuario administrador inicial")
            admin = User(
                email="admin@smartacademy.com",
                hashed_password=get_password_hash("admin123"),  # Cambiar esta contraseña en producción
                full_name="Administrador",
                is_active=True,
                is_superuser=True,
                role=RoleEnum.ADMINISTRATOR
            )
            db.add(admin)
            db.commit()
            logger.info(f"Usuario administrador creado con email: {admin.email}")
            logger.info("IMPORTANTE: Cambia la contraseña inmediatamente después de iniciar sesión")
        else:
            logger.info("El usuario administrador ya existe, no se requiere inicialización")
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Inicializando la base de datos")
    init_db()
    logger.info("Base de datos inicializada")
