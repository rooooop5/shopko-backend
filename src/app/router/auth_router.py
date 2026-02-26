from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session,select
from app.db.seeds.seed_tables import get_session
from app.auth.security import create_access_token, authenticate_user
from app.models.user_models import UserRegister,UserLogin,UserResponse,Users
from app.models.enums import RolesEnum
from app.endpoints.auth_endpoints import login_endpoint, register_endpoint

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
def msg():
    return "This is the default route of the auth router."


@auth_router.post("/register",status_code=201)
def register(user: UserRegister, session: Session = Depends(get_session)):
    return register_endpoint(user=user, session=session)

@auth_router.post("/token")
def login(user:OAuth2PasswordRequestForm=Depends(OAuth2PasswordRequestForm),session:Session=Depends(get_session)):
    pass

@auth_router.post("/select-role")
def set_role(role:RolesEnum):
    pass