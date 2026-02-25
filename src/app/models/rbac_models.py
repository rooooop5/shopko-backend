from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, TYPE_CHECKING
from app.models.user_models import UsersRoles

if TYPE_CHECKING:
    from app.models.user_models import Users


class RolesEnum(str, Enum):
    MODERATOR = "moderator"
    SELLER = "seller"
    CUSTOMER = "customer"


class PermissionsEnum(Enum):
    viewProducts = "view_products"  # customer,seller,moderator
    listProduct = "list_product"  # seller
    getProduct = "get_product"  # customer,seller,moderator
    placeOrder = "place_order"  # customer
    viewOrder = "view_order"  # customer,seller
    listOrders = "list_orders"  # customer,seller
    cancelOrder = "cancel_order"  # customer,seller
    updateProduct = "update_product"  # seller
    viewSeller = "view_seller"  # moderator
    removeSeller = "remove_seller"  # moderator
    viewCustomer = "view_customer"  # moderator
    removeCustomer = "remove_customer"  # moderator
    removeProduct = "remove_product"  # seller,moderator


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
