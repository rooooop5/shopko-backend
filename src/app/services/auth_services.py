import json
from sqlmodel import Session,select
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schemas import UserRegister, UserCreatedResponse,UserLoggedInResponse
from app.models.user_models import Users,UsersRoles
from app.core.exceptions import user_already_exists_exception,role_not_allowed_exception
from app.core.enums import RolesEnum
from app.models.rbac_models import Roles
from app.auth.password_utils import hash_password
from app.auth.security import create_access_token,verify_login_request,Token


def login_endpoint(user:OAuth2PasswordRequestForm, session: Session):
    db_user:Users=verify_login_request(user=user,session=session)
    access_token=create_access_token(data={"sub":db_user.username})
    return Token(access_token=access_token,token_type="bearer")
    

def me(db_user:Users):
    roles=[item.role for item in db_user.roles ]
    response={"username":db_user.username,"email":db_user.email,"roles":roles}
    return UserLoggedInResponse.model_validate(response)

def register_endpoint(user: UserRegister,roles:list[RolesEnum], session: Session):
    user.password = hash_password(user.password)
    db_user = Users(**user.model_dump())
    try:
        session.add(db_user)
        session.flush()
        for role in roles:
            role_query=session.exec(select(Roles).where(Roles.role==role)).one()
            user_role={"user":db_user.id,"role":role_query.id}
            db_user_roles=UsersRoles.model_validate(user_role)
            session.add(db_user_roles)
        session.commit()
    except IntegrityError:
        raise user_already_exists_exception
    session.refresh(db_user)
    response = UserCreatedResponse.model_validate(db_user)
    return JSONResponse(content={"user_details": response.model_dump()})

def set_role(db_user:Users,role):
    permissable_roles=[items.role for items in db_user.roles]
    if role in permissable_roles:
        role_access_token=create_access_token(data={"sub":db_user.username,"role":role})
        return Token(access_token=role_access_token,token_type="bearer")
    else:
        raise role_not_allowed_exception
    