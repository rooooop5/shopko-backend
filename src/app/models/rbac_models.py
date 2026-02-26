from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, TYPE_CHECKING
from app.models.user_models import UsersRoles
from app.models.enums import RolesEnum, PermissionsEnum

if TYPE_CHECKING:
    from app.models.user_models import Users


class RolePermissions(SQLModel, table=True):
    role: Annotated[int, Field(foreign_key="roles.id", primary_key=True)]
    permission: Annotated[int, Field(foreign_key="permissions.id", primary_key=True)]


role_permissions_mapping = {
    RolesEnum.MODERATOR: [
        PermissionsEnum.viewProducts,
        PermissionsEnum.getProduct,
        PermissionsEnum.viewSeller,
        PermissionsEnum.removeSeller,
        PermissionsEnum.viewCustomer,
        PermissionsEnum.removeCustomer,
        PermissionsEnum.removeProduct,
    ],
    RolesEnum.CUSTOMER: [
        PermissionsEnum.viewProducts,
        PermissionsEnum.getProduct,
        PermissionsEnum.placeOrder,
        PermissionsEnum.viewOrder,
        PermissionsEnum.listOrders,
        PermissionsEnum.cancelOrder,
    ],
    RolesEnum.SELLER: [
        PermissionsEnum.viewProducts,
        PermissionsEnum.listProduct,
        PermissionsEnum.getProduct,
        PermissionsEnum.viewOrder,
        PermissionsEnum.listOrders,
        PermissionsEnum.cancelOrder,
        PermissionsEnum.updateProduct,
        PermissionsEnum.removeProduct,
    ],
}


class Permissions(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    permission: Annotated[str, Field(unique=True)]
    roles: list["Roles"] = Relationship(back_populates="permissions", link_model=RolePermissions)


class Roles(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    role: Annotated[str, Field(unique=True)]
    permissions: list["Permissions"] = Relationship(back_populates="roles", link_model=RolePermissions)
    users: list["Users"] = Relationship(back_populates="roles", link_model=UsersRoles)
