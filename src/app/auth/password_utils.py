from passlib.context import CryptContext
from src.env_utils import Settings

crypt_context = CryptContext(schemes=[Settings.HASHING_ALGORITHM], deprecated="auto")


def hash_password(password: str):
    return crypt_context.hash(secret=password)


def verify_password(password: str, hashed_password: str):
    return crypt_context.verify(secret=password, hash=hashed_password)
