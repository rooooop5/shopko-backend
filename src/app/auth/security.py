import jwt
from jwt.exceptions import InvalidTokenError,InvalidSubjectError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from pydantic import BaseModel
from app.db.seeds.seed_tables import engine
from app.auth.settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(payload=to_encode, key=Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return token

def verify_login_request():
    pass

def authenticate_user(session: Session, token=Depends(oauth2_scheme)):
    try:
        payload= jwt.decode(token, Settings.SECRET_KEY, Settings.ALGORITHM)
        sub=payload.get("sub")
        if not sub:
            raise InvalidSubjectError
            
    except InvalidTokenError:
        raise InvalidTokenError


