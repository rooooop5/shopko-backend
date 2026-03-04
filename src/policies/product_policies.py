from sqlmodel import Session, select
from core.enums import RolesEnum, PermissionsEnum
from db.models.user_models import Users
from db.models.rbac_models import Roles
from db.models.product_model import Products


class ProductPolicy:
    def __init__(self, user, active_role: RolesEnum, product: Products, session: Session):
        self.user = user
        self.active_role = active_role
        self.product = product
        self.session = session
        self.role_permissions = self._load_permissions()

    def _load_permissions(self):
        """
        Fetch all permissions related to the active role
        """
        role = self.session.exec(select(Roles).where(Roles.role == self.active_role)).one()
        permissions = [permission.permission for permission in role.permissions]
        return permissions

    def can_list(self):
        if PermissionsEnum.viewOrder.value in self.role_permissions:
            return True
        return False
