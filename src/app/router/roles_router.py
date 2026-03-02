from fastapi import APIRouter,Depends
from sqlmodel import Session
from schemas.rbac_schemas import ActiveRoleResponse
from app.auth.security import Token,authenticate_role,authenticate_user
from core.enums import RolesEnum
from db.models.user_models import Users
from db.seeds.seed_tables import get_session
from services.rbac.roles_services import set_role
from services.rbac.permissions_services import get_active_permissions
roles_router=APIRouter(prefix="/role",tags=["role"])


@roles_router.post("/select-role", response_model=Token)
def select_role_endpoint(role: RolesEnum, db_user: Users = Depends(authenticate_user)):
    role_access_token = set_role(db_user=db_user, role=role)
    return Token(access_token=role_access_token, token_type="bearer")


@roles_router.get("/active-role", response_model=ActiveRoleResponse)
def get_active_role_endpoint(active_role=Depends(authenticate_role)):
    return ActiveRoleResponse.model_validate(active_role)


@roles_router.get("/active-permissions")
def get_active_permissions_endpoint(active_role=Depends(authenticate_role), session:Session=Depends(get_session)):
    active_permissions = get_active_permissions(active_role_dict=active_role, session=session)
    return active_permissions