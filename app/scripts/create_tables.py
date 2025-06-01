import logging
from sqlalchemy import inspect, text

from app.config.database import engine
from app.db.base import Base
from app.models.user import User
from app.models.role import Role
# Comentado temporalmente hasta implementación futura
# from app.models.device import UserDevice, UserNotificationPreference
# from app.models.notification import Notification
# Importar aquí el resto de modelos para asegurar que se creen todas las tablas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Crea todas las tablas definidas en los modelos si no existen"""
    try:
        logger.info("Verificando tablas existentes...")
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        logger.info(f"Tablas existentes: {existing_tables}")
        
        if "users" not in existing_tables:
            logger.info("Creando tablas en la base de datos...")
            Base.metadata.create_all(bind=engine)
            logger.info("Tablas creadas exitosamente")
        else:
            logger.info("Las tablas ya existen, no es necesario crearlas")
    except Exception as e:
        logger.error(f"Error al crear tablas: {e}")

if __name__ == "__main__":
    logger.info("Iniciando creación de tablas...")
    create_tables()
    logger.info("Proceso completado")
