from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.associations import user_role

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    permissions = Column(JSON)  # Almacenará un JSON con los permisos específicos
    
    # Relación con usuarios
    users = relationship("User", secondary=user_role, back_populates="roles")
