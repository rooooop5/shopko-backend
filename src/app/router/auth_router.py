from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List
from db.seeds.seed_tables import get_session
from schemas.user_schemas import UserRegister, UserCreatedResponse, UserLoggedInResponse
from db.models.user_models import Users
from schemas.rbac_schemas import ActiveRoleResponse
from core.enums import RolesEnum
from services.auth.auth_services import login, register, me
from services.rbac.roles_services import set_role
from services.rbac.permissions_services import get_active_permissions
from app.auth.security import Token, authenticate_user, authenticate_role

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=201, response_model=UserCreatedResponse)
def register_endpoint(user: UserRegister, roles: List[RolesEnum] = Query(), session: Session = Depends(get_session)):
    response = register(new_user=user, requested_roles=roles, session=session)
    return UserCreatedResponse.model_validate(response)


@auth_router.post("/token", response_model=Token, summary="Route Login Access Token Post")
def login_endpoint(
    user: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), session: Session = Depends(get_session)
):
    access_token = login(user=user, session=session)
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/whoami", response_model=UserLoggedInResponse)
def get_current_user_endpoint(db_user: Users = Depends(authenticate_user)):
    current_user = me(db_user=db_user)
    return UserLoggedInResponse.model_validate(current_user)
