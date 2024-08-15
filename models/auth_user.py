#
from __future__ import annotations
from sqlalchemy import Integer, String, Column
from pydantic   import BaseModel

from database import BaseClass


class AuthUser(BaseClass):
    __tablename__ = "auth_users"

    id       = Column(Integer, primary_key = True)
    email    = Column(String, unique = True, index = True)
    password = Column(String)
    name     = Column(String, index = True, nullable = True)
    address  = Column(String, nullable = True)
    phone    = Column(String, unique = True, nullable = True)

class BaseAuthUserDTO(BaseModel):
    email: str
    name: str | None = None
    address: str | None = None
    phone: str | None = None

class RegisterInputDTO(BaseAuthUserDTO):
    password: str

class AuthUserDTO(BaseAuthUserDTO):
    id: int

    class Config:
        orm_mode = True

class LoginResponseDTO(BaseModel):
    login_token: str
