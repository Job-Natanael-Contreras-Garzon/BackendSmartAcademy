from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.associations import user_role
import enum

class GenderEnum(str, enum.Enum):
    FEMALE = "FEMALE"
    MALE = "MALE"
    OTHER = "OTHER"

class RoleEnum(str, enum.Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    PARENT = "PARENT"
    ADMINISTRATOR = "ADMINISTRATOR"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    phone = Column(String, nullable=True)
    direction = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    gender = Column(SQLEnum(GenderEnum), default=GenderEnum.OTHER)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.STUDENT)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relaciones (se configurarán cuando implementemos las tablas relacionadas)
    roles = relationship("Role", secondary=user_role, back_populates="users")
    
    # Relaciones con dispositivos y preferencias de notificaciones
    devices = relationship("UserDevice", back_populates="user", cascade="all, delete-orphan")
    notification_preferences = relationship("UserNotificationPreference", back_populates="user", cascade="all, delete-orphan", uselist=False)
    
    # Relaciones con notificaciones
    received_notifications = relationship("Notification", foreign_keys="[Notification.recipient_id]", backref="recipient")
    sent_notifications = relationship("Notification", foreign_keys="[Notification.sender_id]", backref="sender")
    
    # Nota: Estas relaciones se implementarán cuando los modelos correspondientes existan
    # tutored_students = relationship("StudentTutor", back_populates="tutor")