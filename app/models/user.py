from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.associations import user_role
import enum

class GenderEnum(str, enum.Enum):
    FEMALE = "female"
    MALE = "male"
    OTHER = "other"

class RoleEnum(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"
    ADMINISTRATOR = "administrator"

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
    gender = Column(Enum(GenderEnum), default=GenderEnum.OTHER)
    role = Column(Enum(RoleEnum), default=RoleEnum.STUDENT)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relaciones (se configurarán cuando implementemos las tablas relacionadas)
    roles = relationship("Role", secondary=user_role, back_populates="users")
    
    # Nota: Estas relaciones se implementarán cuando los modelos correspondientes existan
    # tutored_students = relationship("StudentTutor", back_populates="tutor")