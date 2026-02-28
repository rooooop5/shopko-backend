import jwt
from jwt.exceptions import InvalidTokenError, InvalidSubjectError
from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from pydantic import BaseModel
from app.models.user_models import Users
from app.auth.settings import Settings
from app.core.exceptions import credentials_exception,user_does_not_exist_exception
from app.db.seeds.seed_tables import get_session
from app.auth.password_utils import verify_password



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(payload=to_encode, key=Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return token


def verify_login_request(user: OAuth2PasswordRequestForm, session: Session):
    try:
        query = select(Users).where(Users.username == user.username)
        db_user = session.exec(query).one()
    except NoResultFound:
        raise credentials_exception
    if not verify_password(user.password, db_user.password):
        raise credentials_exception
    return db_user


def authenticate_user(token=Depends(oauth2_scheme),session:Session=Depends(get_session)):
    try:
        payload = jwt.decode(jwt=token,key=Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    try:
        query=select(Users).where(Users.username==username)
        db_user=session.exec(query).one()
    except NoResultFound:
        raise user_does_not_exist_exception
    return db_user
