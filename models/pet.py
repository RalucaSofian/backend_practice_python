#

from sqlalchemy       import Integer, Float, String, Column
from pydantic         import BaseModel
from sqlalchemy_utils import TSVectorType

from database import BaseClass
from utils    import generic_exceptions as GenException



class BasePetDTO(BaseModel):
    name: str
    species: str | None = None
    gender: str | None = None
    age: float | None = None
    description: str | None = None


class PetDTO(BasePetDTO):
    id:int

    class Config:
        orm_mode = True


class Pet(BaseClass):
    __tablename__ = "pets"

    id            = Column(Integer, primary_key = True)
    name          = Column(String)
    species       = Column(String, nullable = True)
    gender        = Column(String, nullable = True)
    age           = Column(Float, nullable = True)
    description   = Column(String, nullable = True)
    search_vector = Column(TSVectorType("name", "species", "gender", "description"))

    def __init__(self, pet: BasePetDTO):
        self.name = pet.name
        self.species = pet.species
        self.gender = pet.gender
        self.age = pet.age
        self.description = pet.description

    @classmethod
    def field(klass, field_name: str):
        match field_name:
            case "id":
                return Pet.id
            case "name":
                return Pet.name
            case "species":
                return Pet.species
            case "gender":
                return Pet.gender
            case "age":
                return Pet.age
            case "description":
                return Pet.description
            case _:
                raise GenException.FieldErrorException
