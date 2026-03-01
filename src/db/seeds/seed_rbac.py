from sqlmodel import Session, select
from db.models.rbac_models import Permissions, Roles, RolePermissions
from core.enums import RolesEnum, PermissionsEnum
from schemas.rbac_schemas import role_permissions_mapping
from sqlalchemy.exc import IntegrityError


def seed_permissions(session: Session):
    for perm in PermissionsEnum:
        permission_instance = Permissions(permission=perm.value)
        try:
            session.add(permission_instance)
            session.commit()
        except IntegrityError:
            session.rollback()


def seed_roles(session: Session):
    for roles in RolesEnum:
        try:
            role_instance = Roles(role=roles.value)
            session.add(role_instance)
            session.commit()
        except IntegrityError:
            session.rollback()


def seed_roles_permissions(session: Session):
    for role in role_permissions_mapping:
        db_role = session.exec(select(Roles).where(Roles.role == role.value)).first()
        for permission in role_permissions_mapping[role]:
            db_permission = session.exec(select(Permissions).where(Permissions.permission == permission.value)).first()
            role_permission_instance = RolePermissions(role=db_role.id, permission=db_permission.id)
            try:
                session.add(role_permission_instance)
                session.commit()
            except IntegrityError:
                session.rollback()
