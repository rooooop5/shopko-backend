import jwt
from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List
from db.seeds.seed_tables import get_session
from schemas.user_schemas import UserRegister, UserCreatedResponse, UserLoggedInResponse
from db.models.user_models import Users
from schemas.rbac_schemas import ActiveRoleResponse
from core.enums import RolesEnum
from services.auth_services import login_endpoint, register_endpoint, me, set_role_endpoint
from app.auth.security import Token, authenticate_user, authenticate_role

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=201, response_model=UserCreatedResponse)
def register(user: UserRegister, roles: List[RolesEnum] = Query(), session: Session = Depends(get_session)):
    response = register_endpoint(user=user, roles=roles, session=session)
    return UserCreatedResponse.model_validate(response)


@auth_router.post("/token", response_model=Token, summary="Route Login Access Token Post")
def login(
    user: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), session: Session = Depends(get_session)
):
    access_token = login_endpoint(user=user, session=session)
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/whoami", response_model=UserLoggedInResponse)
def get_current_user(db_user: Users = Depends(authenticate_user)):
    current_user = me(db_user=db_user)
    return UserLoggedInResponse.model_validate(current_user)


@auth_router.post("/select-role", response_model=Token)
def select_role(role: RolesEnum, db_user: Users = Depends(authenticate_user)):
    role_access_token = set_role_endpoint(db_user=db_user, role=role)
    return Token(access_token=role_access_token, token_type="bearer")


@auth_router.get("/active-role", response_model=ActiveRoleResponse)
def get_active_role(active_role=Depends(authenticate_role)):
    return ActiveRoleResponse.model_validate(active_role)
