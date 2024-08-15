# calls to methods from /services; format output; validate input

from sqlalchemy.orm import Session
from fastapi        import HTTPException

from models   import auth_user
from services import auth as AuthService


#
def register(register_input: auth_user.RegisterInputDTO, db: Session):
    try:
        return AuthService.register_user(db, register_input)
    except AuthService.UserExistsException as e:
        print(e)
        raise HTTPException(status_code = 400, detail = "User Already Exists")

#
def login(login_input: auth_user.RegisterInputDTO, db: Session):
    token = AuthService.login_user(db, login_input)
    if token is None:
        raise HTTPException(status_code = 401, detail = "Unauthorized")
    return auth_user.LoginResponseDTO(login_token = token)

#
def get_user(user_id: int, db: Session):
    user = AuthService.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code = 404, detail = "Not Found")
    return user

#
def get_users(limit_users: int, db: Session):
    return AuthService.get_users(db, limit_users)

#
def update_user(user_id: int, update_input: dict[str, object], db: Session):
    try:
        return AuthService.update_user(db, user_id, update_input)
    except AuthService.UserDoesNotExistException as e:
        print(e)
        raise HTTPException(status_code = 404, detail = "Not Found")
    except AuthService.UpdateUserFailException as e:
        print(e)
        raise HTTPException(status_code = 400, detail = "Update Failed")
    except Exception as e:
        print("Unknown Error")
        raise HTTPException(status_code = 500, detail = "Update Failed")

#
def delete_user(user_id: int, db: Session):
    try:
        return AuthService.delete_user(db, user_id)
    except AuthService.DeleteUserFailException as e:
        print(e)
        raise HTTPException(status_code = 404, detail = "Delete Failed")
    except Exception as e:
        print("Unknown Error")
        raise HTTPException(status_code = 500, detail = "Delete Failed")
