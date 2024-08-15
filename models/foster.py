#
from __future__     import annotations
from sqlalchemy     import Integer, String, Column, ForeignKey, Date
from sqlalchemy.orm import relationship
from pydantic       import BaseModel
from datetime       import date

from database  import BaseClass
from models.auth_user import AuthUserDTO
from models.pet       import PetDTO


class Foster(BaseClass):
    __tablename__ = "foster"

    id            = Column(Integer, primary_key = True)
    user_id       = Column("user_id", ForeignKey("auth_users.id"), nullable = True)
    description   = Column(String, nullable = True)
    pet_id        = Column("pet_id", ForeignKey("pets.id"))
    start_date    = Column(Date)
    end_date      = Column(Date, nullable = True)

    user = relationship("AuthUser")
    pet  = relationship("Pet")

class BaseFosterDTO(BaseModel):
    user_id: int | None = None
    description: str | None = None
    pet_id: int
    start_date: date
    end_date: date | None = None

class FosterDTO(BaseFosterDTO):
    id: int
    user: AuthUserDTO | None = None
    pet: PetDTO

    class Config:
        orm_mode = True

class CreateFosterDTO(BaseFosterDTO):
    pass
