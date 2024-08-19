# makes calls to database

from sqlalchemy.orm import Session
from sqlalchemy     import update, delete

from models import foster


class FosterDoesNotExistException(Exception):
    pass

class UpdateFosterFailException(Exception):
    pass

class DeleteFosterFailException(Exception):
    pass


#
def create_foster(db: Session, create_input: foster.CreateFosterDTO):
    db_foster = foster.Foster(pet_id = create_input.pet_id,
                              start_date = create_input.start_date)
    db.add(db_foster)
    db.commit()
    db.refresh(db_foster)
    return db_foster

#
def get_foster(db: Session, foster_id: int):
    db_foster = db.query(foster.Foster).get(foster_id)
    return db_foster

#
def get_all_foster(db: Session, limit_foster: int):
    return db.query(foster.Foster).limit(limit_foster).all()

#
def update_foster(db: Session, foster_id: int, update_input: dict[str, object]):
    if not db.query(foster.Foster).filter(foster.Foster.id == foster_id).count() > 0:
        raise FosterDoesNotExistException()
    upd_statement = update(foster.Foster).where(foster.Foster.id == foster_id).values(update_input)
    try:
        db.execute(upd_statement)
    except Exception as e:
        print(e)
        raise UpdateFosterFailException()
    db.commit()
    return get_foster(db, foster_id)

#
def delete_foster(db: Session, foster_id: int):
    del_statement = delete(foster.Foster).where(foster.Foster.id == foster_id)
    if db.query(foster.Foster).filter(foster.Foster.id == foster_id).count() > 0:
        db.execute(del_statement)
        db.commit()
        return "Delete Success"
    raise DeleteFosterFailException()
