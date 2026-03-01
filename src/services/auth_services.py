from sqlmodel import Session, select
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schemas import UserRegister, UserCreatedResponse, UserLoggedInResponse
from app.models.user_models import Users, UsersRoles
from app.core.enums import RolesEnum
from app.models.rbac_models import Roles
from app.auth.password_utils import hash_password
from app.auth.security import create_access_token, verify_login_request, verify_role, Token


def login_endpoint(user: OAuth2PasswordRequestForm, session: Session):
    db_user: Users = verify_login_request(user=user, session=session)
    access_token = create_access_token(data={"sub": db_user.username})
    return access_token


def me(db_user: Users):
    roles = [item.role for item in db_user.roles]
    response = {"username": db_user.username, "email": db_user.email, "roles": roles}
    return response


def register_endpoint(user: UserRegister, roles: list[RolesEnum], session: Session):
    user.password = hash_password(user.password)
    db_user = Users(**user.model_dump())
    session.add(db_user)
    session.flush()
    for role in roles:
        role_query = session.exec(select(Roles).where(Roles.role == role)).one()
        user_role = {"user": db_user.id, "role": role_query.id}
        db_user_roles = UsersRoles.model_validate(user_role)
        session.add(db_user_roles)
    #session.commit()
    session.flush()
    session.refresh(db_user)
    response = {"username": db_user.username, "email": db_user.email}
    return response


def set_role_endpoint(db_user: Users, role):
    verify_role(db_user=db_user, role=role)
    role_access_token = create_access_token(data={"sub": db_user.username, "role": role})
    return role_access_token
