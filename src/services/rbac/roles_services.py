from sqlmodel import Session,select
from typing import List
from core.enums import RolesEnum
from db.models.rbac_models import Roles,UsersRoles
from db.models.user_models import Users
from app.auth.security import verify_role,create_access_token

def get_all_roles(db_user:Users):
       roles = [item.role for item in db_user.roles]
       return roles

def create_user_roles(db_user:Users,roles:List[RolesEnum],session:Session):
    for role in roles:
        roles_query = select(Roles).where(Roles.role == role)
        db_roles=session.exec(roles_query).one()
        user_role = {"user": db_user.id, "role": db_roles.id}
        db_user_roles = UsersRoles.model_validate(user_role)
        return db_user_roles
    
def set_role_endpoint(db_user: Users, role):
    verify_role(db_user=db_user, role=role)
    role_access_token = create_access_token(data={"sub": db_user.username, "role": role})
    return role_access_token