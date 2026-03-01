import jwt
from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List
from app.db.seeds.seed_tables import get_session
from app.schemas.user_schemas import UserRegister, UserCreatedResponse, UserLoggedInResponse
from app.models.user_models import Users
from app.schemas.rbac_schemas import ActiveRoleResponse
from app.core.enums import RolesEnum
from app.services.auth_services import login_endpoint, register_endpoint, me,set_role
from app.auth.security import Token, authenticate_user,authenticate_role

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=201, response_model=UserCreatedResponse)
def register(user: UserRegister, roles: List[RolesEnum] = Query(), session: Session = Depends(get_session)):
    return register_endpoint(user=user, roles=roles, session=session)


@auth_router.post("/token", response_model=Token, summary="Route Login Access Token Post")
def login(
    user: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), session: Session = Depends(get_session)
):
    return login_endpoint(user=user, session=session)


@auth_router.get("/whoami",response_model=UserLoggedInResponse)
def get_current_user(db_user: Users = Depends(authenticate_user)):
    return me(db_user=db_user)


@auth_router.post("/select-role",response_model=Token)
def select_role(role: RolesEnum,db_user:Users=Depends(authenticate_user)):
    return set_role(db_user=db_user,role=role)

@auth_router.get("/active-role",response_model=ActiveRoleResponse)
def get_active_role(role=Depends(authenticate_role)):
    return role
