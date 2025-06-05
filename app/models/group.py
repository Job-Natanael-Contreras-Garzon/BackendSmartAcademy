from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from app.db.base import Base
from app.schemas.group import GradeEnum, LevelEnum 

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(SQLAlchemyEnum(GradeEnum, name="grade_enum_groups", create_type=False), nullable=False)
    level = Column(SQLAlchemyEnum(LevelEnum, name="level_enum_groups", create_type=False), nullable=False)
    group_name = Column(String(50), nullable=False)
