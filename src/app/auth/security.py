import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from pydantic import BaseModel
from app.models.user_models import Users
from app.schemas.rbac_schemas import ActiveRoleResponse
from app.auth.settings import Settings
from exception_handlers.http_exception_handler.http_exceptions import (
    credentials_exception,
    user_does_not_exist_exception,
    incorrect_password_exception,
    role_not_allowed_exception,
)
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
        raise user_does_not_exist_exception
    if not verify_password(user.password, db_user.password):
        raise incorrect_password_exception
    return db_user


def authenticate_user(token=Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(jwt=token, key=Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    try:
        query = select(Users).where(Users.username == username)
        db_user = session.exec(query).one()
    except NoResultFound:
        raise user_does_not_exist_exception
    return db_user


def verify_role(db_user:Users, role):
    permissable_roles = [items.role for items in db_user.roles]
    if not role in permissable_roles:
        raise role_not_allowed_exception


def authenticate_role(token=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(jwt=token, key=Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        role = payload.get("role")
        if not role:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return {"active_role": role}
