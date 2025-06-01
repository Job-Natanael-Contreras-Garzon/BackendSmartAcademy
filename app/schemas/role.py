from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Dict[str, Any] = {}

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None

class RoleResponse(RoleBase):
    id: int

    class Config:
        orm_mode = True

class RoleAssignment(BaseModel):
    role_id: int
