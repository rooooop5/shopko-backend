from sqlmodel import Session,select
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schemas import UserRegister, UserLogin, UserCreatedResponse,UserLoggedInResponse
from app.models.user_models import Users,UsersRoles
from app.core.exceptions import credentials_exception,user_already_exists_exception
from app.core.enums import RolesEnum
from app.models.rbac_models import Roles
from app.auth.password_utils import hash_password, verify_password


def login_endpoint(user:OAuth2PasswordRequestForm, session: Session):
    try:
        query=select(Users).where(Users.username==user.username)
        db_user=session.exec(query).one()
    except:
        raise credentials_exception
    if not verify_password(user.password,db_user.password):
        raise credentials_exception
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
