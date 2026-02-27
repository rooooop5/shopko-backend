from fastapi import APIRouter, Depends,Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List
from app.db.seeds.seed_tables import get_session
from app.models.user_models import UserRegister, UserLogin, UserCreatedResponse, Users
from app.models.enums import RolesEnum
from app.endpoints.auth_endpoints import login_endpoint, register_endpoint

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=201)
def register(user: UserRegister,roles:List[RolesEnum]=Query(), session: Session = Depends(get_session)):
    return register_endpoint(user=user,roles=roles, session=session)


@auth_router.post("/token")
def login(
    user: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), session: Session = Depends(get_session)
):
    return login_endpoint(user=user, session=session)


@auth_router.post("/select-role")
def set_role(role: RolesEnum):
    pass
