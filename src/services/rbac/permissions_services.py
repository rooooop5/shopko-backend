from sqlmodel import Session, select
from db.models.rbac_models import RolePermissions, Roles



def get_active_permissions(active_role_dict, session: Session):
    active_role=active_role_dict["active_role"]
    role_query = select(Roles).where(Roles.role == active_role)
    db_role = session.exec(role_query).one()
    response = {"active_role": active_role, "permissions": [permission.permission for permission in db_role.permissions]}
    return response
