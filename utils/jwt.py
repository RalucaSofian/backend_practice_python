#

import jwt
from datetime import datetime, timezone, timedelta

from utils import constants

def create_access_token(data: dict, expires_minutes: int = constants.ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = expires_minutes)
    to_encode.update({"expires": expire.isoformat()})
    return jwt.encode(to_encode, constants.SECRET_KEY, constants.ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token, constants.SECRET_KEY, constants.ALGORITHM)

def is_token_valid(token: str):
    decoded_token = decode_access_token(token = token)
    token_expiration = decoded_token['expires']

    if datetime.now(timezone.utc) < datetime.fromisoformat(token_expiration):
        print("Token Valid")
        return True
    else:
        print("Token Expired")
        return False
