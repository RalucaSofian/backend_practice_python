# makes calls to database

from sqlalchemy.orm import Session
from sqlalchemy     import update, delete

from models import auth_user, client
from utils  import hashing as Hashing, jwt as JWT


class UserExistsException(Exception):
    pass

class UserDoesNotExistException(Exception):
    pass

class UpdateUserFailException(Exception):
    pass

class DeleteUserFailException(Exception):
    pass


#
def register_user(db: Session, register_input: auth_user.RegisterInputDTO):
    db_user = auth_user.AuthUser(
        email = register_input.email,
        password = register_input.password,
        name = register_input.name,
        address = register_input.address,
        phone = register_input.phone
    )
    if db.query(auth_user.AuthUser).filter(auth_user.AuthUser.email == register_input.email).count() > 0:
        raise UserExistsException()
    db_user.password = Hashing.get_password_hash(db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # create Client obj for crt user
    db_client = client.Client(user_id = db_user.id, description = f"{db_user.name} ({db_user.phone})")
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_user

#
def login_user(db: Session, login_input: auth_user.RegisterInputDTO):
    db_user = db.query(auth_user.AuthUser).filter(auth_user.AuthUser.email == login_input.email).first()
    if db_user is not None and Hashing.verify_password(login_input.password, db_user.password):
        return JWT.create_access_token({"email" : login_input.email})
    else:
        return None

#
def get_user(db: Session, user_id: int):
    db_user = db.query(auth_user.AuthUser).get(user_id)
    return db_user

#
def get_users(db: Session, limit_users: int):
    return db.query(auth_user.AuthUser).limit(limit_users).all()

#
def update_user(db: Session, user_id: int, update_input: dict[str, object]):
    if not db.query(auth_user.AuthUser).filter(auth_user.AuthUser.id == user_id).count() > 0:
        raise UserDoesNotExistException()
    upd_statement = update(auth_user.AuthUser).where(auth_user.AuthUser.id == user_id).values(update_input)
    try:
        db.execute(upd_statement)
    except Exception as e:
        print(e)
        raise UpdateUserFailException()
    db.commit()
    return get_user(db, user_id)

#
def delete_user(db: Session, user_id: int):
    del_statement = delete(auth_user.AuthUser).where(auth_user.AuthUser.id == user_id)
    if db.query(auth_user.AuthUser).filter(auth_user.AuthUser.id == user_id).count() > 0:
        db.execute(del_statement)
        db.commit()
        return "Delete Success"
    raise DeleteUserFailException()
