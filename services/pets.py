# makes calls to database

from sqlalchemy.orm import Session
from sqlalchemy     import update, delete, asc, desc

from models.pet import Pet, BasePetDTO
from utils      import query as QueryUtil


class PetDoesNotExistException(Exception):
    pass

class UpdatePetFailException(Exception):
    pass

class DeletePetFailException(Exception):
    pass



#
def create_pet(db: Session, create_input: BasePetDTO):
    db_pet = Pet(create_input)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


#
def get_pet(db: Session, pet_id: int):
    db_pet = db.query(Pet).get(pet_id)
    return db_pet


#
def get_pets(db: Session, query_info: QueryUtil.QueryInfo, limit_pets: int):
    query = db.query(Pet)

    if query_info.search != None:
        query = query.filter(Pet.search_vector.match(query_info.search))

    if query_info.order != None:
        field = Pet.field(query_info.order.field)
        if query_info.order.direction == QueryUtil.OrderDirection.ASC:
            query = query.order_by(asc(field))
        elif query_info.order.direction == QueryUtil.OrderDirection.DESC:
            query = query.order_by(desc(field))
        else:
            query = query.order_by(asc(field))

    if query_info.limit != None:
        query = query.limit(query_info.limit)
    else:
        query = query.limit(limit_pets)

    if query_info.offset != None:
        query = query.offset(query_info.offset)
    else:
        query = query.offset(0)

    for filter in query_info.filters:
        field = Pet.field(filter.field)
        if filter.operation == QueryUtil.FilterOperation.EQ:
            query = query.where(field == filter.value)
        elif filter.operation == QueryUtil.FilterOperation.GT:
            query = query.where(field > filter.value)
        elif filter.operation == QueryUtil.FilterOperation.GTE:
            query = query.where(field >= filter.value)
        elif filter.operation == QueryUtil.FilterOperation.LT:
            query = query.where(field < filter.value)
        elif filter.operation == QueryUtil.FilterOperation.LTE:
            query = query.where(field <= filter.value)
        elif filter.operation == QueryUtil.FilterOperation.IS_NULL:
            if filter.value == True:
                query = query.where(field == None)
            elif filter.value == False:
                query = query.where(field != None)
        elif filter.operation == QueryUtil.FilterOperation.IN:
            query = query.where(field.in_(filter.value))
        elif filter.operation == QueryUtil.FilterOperation.NOT_IN:
            query = query.where(field.not_in(filter.value))

    return query


#
def update_pet(db: Session, pet_id: int, update_input: dict[str, object]):
    if not db.query(Pet).filter(Pet.id == pet_id).count() > 0:
        raise PetDoesNotExistException()
    upd_statement = update(Pet).where(Pet.id == pet_id).values(update_input)
    try:
        db.execute(upd_statement)
    except Exception as e:
        print(e)
        raise UpdatePetFailException()
    db.commit()
    return get_pet(db, pet_id)


#
def delete_pet(db: Session, pet_id: int):
    del_statement = delete(Pet).where(Pet.id == pet_id)
    if db.query(Pet).filter(Pet.id == pet_id).count() > 0:
        db.execute(del_statement)
        db.commit()
        return "Delete Success"
    raise DeletePetFailException()
