# calls to methods from /services; format output; validate input

from sqlalchemy.orm import Session
from fastapi        import HTTPException, Request

from models   import pet
from services import pets as PetService
from utils    import query as QueryUtil


#
def create_pet(create_input: pet.BasePetDTO, db: Session):
    return PetService.create_pet(db, create_input)

#
def get_pet(pet_id: int, db: Session):
    pet = PetService.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code = 404, detail = "Not Found")
    return pet

#
def get_pets(request: Request, limit_pets: int, db: Session):
    query_info = QueryUtil.parse_query_params(request)
    if query_info is None:
        print("no query")
    else:
        print(query_info)
    return PetService.get_pets(db, query_info, limit_pets)

#
def update_pet(pet_id: int, update_input: dict[str, object], db: Session):
    try:
        return PetService.update_pet(db, pet_id, update_input)
    except PetService.PetDoesNotExistException as e:
        print(e)
        raise HTTPException(status_code = 404, detail = "Not Found")
    except PetService.UpdatePetFailException as e:
        print(e)
        raise HTTPException(status_code = 400, detail = "Update Failed")
    except Exception as e:
        print("Unknown Error")
        raise HTTPException(status_code = 500, detail = "Update Failed")

#
def delete_pet(pet_id: int, db: Session):
    try:
        return PetService.delete_pet(db, pet_id)
    except PetService.DeletePetFailException as e:
        print(e)
        raise HTTPException(status_code = 404, detail = "Delete Failed")
    except Exception as e:
        print("Unknown Error")
        raise HTTPException(status_code = 500, detail = "Delete Failed")
