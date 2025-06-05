import sys
import os

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import logging
from sqlalchemy import inspect, text

from app.config.database import engine
from app.db.base import Base
from app.models.user import User
from app.models.role import Role
from app.models.subject import Subject
from app.models.course import Course
from app.models.group import Group
from app.models.period import Period
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.grade import Grade
from app.models.attendance import Attendance
from app.models.participation import Participation
# Comentado temporalmente hasta implementación futura
# from app.models.device import UserDevice, UserNotificationPreference
# from app.models.notification import Notification
# Importar aquí el resto de modelos para asegurar que se creen todas las tablas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Crea todas las tablas definidas en los modelos si no existen"""
    try:
        logger.info("Verificando tablas existentes antes de la operación...")
        inspector = inspect(engine)
        existing_tables_before = inspector.get_table_names()
        logger.info(f"Tablas existentes (antes): {existing_tables_before}")
        
        logger.info("Intentando crear todas las tablas definidas en los modelos (si no existen)...")
        # Base.metadata.create_all() es idempotente y no intentará recrear tablas existentes.
        Base.metadata.create_all(bind=engine)
        logger.info("Proceso de creación de tablas completado.")

        logger.info("Verificando tablas existentes después de la operación...")
        existing_tables_after = inspector.get_table_names()
        logger.info(f"Tablas existentes (después): {existing_tables_after}")

    except Exception as e:
        logger.error(f"Error durante el proceso de creación de tablas: {e}")

if __name__ == "__main__":
    logger.info("Iniciando creación de tablas...")
    create_tables()
    logger.info("Proceso completado")
