#
from __future__     import annotations
from sqlalchemy     import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from pydantic       import BaseModel

from database         import BaseClass
from models.auth_user import AuthUserDTO


class Client(BaseClass):
    __tablename__ = "clients"

    id          = Column(Integer, primary_key = True)
    user_id     = Column("user_id", ForeignKey("auth_users.id"), nullable = True)
    description = Column(String, nullable = True)

    user = relationship("AuthUser")

class BaseClientDTO(BaseModel):
    user_id: int | None = None
    description: str | None = None

class ClientDTO(BaseClientDTO):
    id: int
    user: AuthUserDTO | None = None

    class Config:
        orm_mode = True

class CreateClientDTO(BaseClientDTO):
    pass