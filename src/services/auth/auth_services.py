from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user_schemas import UserRegister
from db.models.user_models import Users
from core.enums import RolesEnum
from app.auth.password_utils import hash_password
from app.auth.security import create_access_token, verify_login_request, verify_role
from services.rbac.roles_services import get_all_roles,create_user_roles


def login_endpoint(user: OAuth2PasswordRequestForm, session: Session):
    db_user: Users = verify_login_request(user=user, session=session)
    access_token = create_access_token(data={"sub": db_user.username})
    return access_token


def me(db_user: Users):
    roles=get_all_roles(db_user)
    response = {"username": db_user.username, "email": db_user.email, "roles": roles}
    return response


def register_endpoint(new_user: UserRegister, requested_roles: list[RolesEnum], session: Session):
    new_user.password = hash_password(new_user.password)
    db_user = Users(**new_user.model_dump())
    session.add(db_user)
    session.flush()
    db_user_roles=create_user_roles(db_user=db_user,roles=requested_roles,session=session)
    session.add(db_user_roles)
    session.flush()
    session.refresh(db_user)
    response = {"username": db_user.username, "email": db_user.email}
    return response



