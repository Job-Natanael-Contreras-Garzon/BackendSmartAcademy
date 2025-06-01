from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

# Tabla de asociación entre usuarios y roles
user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)
