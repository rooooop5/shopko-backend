from fastapi import APIRouter, Depends,Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List
from app.db.seeds.seed_tables import get_session
from app.schemas.user_schemas import UserRegister, UserLogin, UserCreatedResponse,UserLoggedInResponse
from app.models.user_models import Users
from app.core.enums import RolesEnum
from app.services.auth_services import login_endpoint, register_endpoint

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=201,response_model=UserCreatedResponse)
def register(user: UserRegister,roles:List[RolesEnum]=Query(), session: Session = Depends(get_session)):
    return register_endpoint(user=user,roles=roles, session=session)


@auth_router.post("/token",response_model=UserLoggedInResponse)
def login(
    user: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), session: Session = Depends(get_session)
):
    return login_endpoint(user=user, session=session)


@auth_router.post("/select-role")
def set_role(role: RolesEnum):
    pass
