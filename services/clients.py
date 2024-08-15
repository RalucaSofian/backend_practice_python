# makes calls to database

from sqlalchemy.orm import Session
from sqlalchemy     import update, delete

from models import client


class ClientDoesNotExistException(Exception):
    pass

class UpdateClientFailException(Exception):
    pass

class DeleteClientFailException(Exception):
    pass


#
def create_client(db: Session, create_input: client.CreateClientDTO):
    db_client = client.Client(user_id = create_input.user_id,
                              description = create_input.description)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

#
def get_client(db: Session, client_id: int):
    db_client = db.query(client.Client).get(client_id)
    return db_client

#
def get_clients(db: Session, limit_clients: int):
    return db.query(client.Client).limit(limit_clients).all()

#
def update_client(db: Session, client_id: int, update_input: dict[str, object]):
    if not db.query(client.Client).filter(client.Client.id == client_id).count() > 0:
        raise ClientDoesNotExistException()
    upd_statement = update(client.Client).where(client.Client.id == client_id).values(update_input)
    try:
        db.execute(upd_statement)
    except Exception as e:
        print(e)
        raise UpdateClientFailException()
    db.commit()
    return get_client(db, client_id)

#
def delete_client(db: Session, client_id: int):
    del_statement = delete(client.Client).where(client.Client.id == client_id)
    if db.query(client.Client).filter(client.Client.id == client_id).count() > 0:
        db.execute(del_statement)
        db.commit()
        return "Delete Success"
    raise DeleteClientFailException()

# QUERY !!!!