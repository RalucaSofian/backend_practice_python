#

from passlib.context import CryptContext


def get_password_hash(plain_password: str):
    password_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
    return password_context.hash(plain_password)

def verify_password(password: str, password_hash: str):
    password_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
    return password_context.verify(password, password_hash)
