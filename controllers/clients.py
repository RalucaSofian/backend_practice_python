# calls to methods from /services; format output; validate input

from sqlalchemy.orm import Session
from fastapi        import HTTPException

from models   import client
from services import clients as ClientService


#
def create_client(create_input: client.CreateClientDTO, db: Session):
    return ClientService.create_client(db, create_input)

#
def get_client(client_id: int, db: Session):
    client = ClientService.get_client(db, client_id)
    if client is None:
        raise HTTPException(status_code = 404, detail = "Not Found")
    return client

#
def get_clients(limit_clients: int, db: Session):
    return ClientService.get_clients(db, limit_clients)

#
def update_client(client_id: int, update_input: dict[str, object], db: Session):
    try:
        return ClientService.update_client(db, client_id, update_input)
    except ClientService.ClientDoesNotExistException as e:
        print(e)
        raise HTTPException(status_code = 404, detail = "Not Found")
    except ClientService.UpdateClientFailException as e:
        print(e)
        raise HTTPException(status_code = 400, detail = "Update Failed")
    except Exception as e:
        print("Unknown Error")
        raise HTTPException(status_code = 500, detail = "Update Failed")

#
def delete_client(client_id: int, db: Session):
    try:
        return ClientService.delete_client(db, client_id)
    except ClientService.DeleteClientFailException as e:
        print(e)
        raise HTTPException(status_code = 404, detail = "Delete Failed")
    except Exception as e:
        print("Unknown Error")
        raise HTTPException(status_code = 500, detail = "Delete Failed")
