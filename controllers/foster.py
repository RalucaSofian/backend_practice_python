# calls to methods from /services; format output; validate input

from sqlalchemy.orm import Session
from fastapi        import HTTPException

from models   import foster
from services import foster as FosterService


#
def create_foster(create_input: foster.CreateFosterDTO, db: Session):
    return FosterService.create_foster(db, create_input)

#
def get_foster(foster_id: int, db: Session):
    foster = FosterService.get_foster(db, foster_id)
    if foster is None:
        raise HTTPException(status_code = 404, detail = "Not Found")
    return foster

#
def get_all_foster(limit_foster: int, db: Session):
    return FosterService.get_all_foster(db, limit_foster)

#
def update_foster(foster_id: int, update_input: dict[str, object], db: Session):
    try:
        return FosterService.update_foster(db, foster_id, update_input)
    except FosterService.FosterDoesNotExistException as e:
        print(e)
        raise HTTPException(status_code = 404, detail = "Not Found")
    except FosterService.UpdateFosterFailException as e:
        print(e)
        raise HTTPException(status_code = 400, detail = "Update Failed")
    except Exception as e:
        print("Unknown Error")
        raise HTTPException(status_code = 500, detail = "Update Failed")

#
def delete_foster(foster_id: int, db: Session):
    try:
        return FosterService.delete_foster(db, foster_id)
    except FosterService.DeleteFosterFailException as e:
        print(e)
        raise HTTPException(status_code = 404, detail = "Delete Failed")
    except Exception as e:
        print("Unknown Error")
        raise HTTPException(status_code = 500, detail = "Delete Failed")
