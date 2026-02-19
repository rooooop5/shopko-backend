from enum import Enum
from sqlmodel import SQLModel,Field,Relationship
from typing import Annotated

class RolesEnum(str, Enum):
    MODERATOR = "moderator"
    SELLER = "seller"
    CUSTOMER = "customer"


class PermissionsEnum(Enum):
    viewProducts = "view_products"
    listProducts = "list_products"
    getProduct = "get_product"
    placeOrder = "place_order"
    cancelOrder = "cancel_order"
    listOwnOrders = "list_own_orders"
    viewOwnOrder = "view_own_order"

class RolePermissions(SQLModel,table=True):
    role:Annotated[int,Field(foreign_key="roles.id",primary_key=True)]
    permission:Annotated[int,Field(foreign_key="permissions.id",primary_key=True)]

role_permissions_mapping={
    RolesEnum.MODERATOR:[],
    RolesEnum.CUSTOMER:[PermissionsEnum.viewProducts,PermissionsEnum.getProduct,PermissionsEnum.viewOwnOrder,PermissionsEnum.listOwnOrders,PermissionsEnum.cancelOrder],
    RolesEnum.SELLER:[PermissionsEnum.listProducts]
}





class Permissions(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    permission: Annotated[str, Field(unique=True)]
    roles:list["Roles"]=Relationship(back_populates="permissions",link_model=RolePermissions)



class Roles(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    role: Annotated[str, Field(unique=True)]
    permissions:list["Permissions"]=Relationship(back_populates="roles",link_model=RolePermissions)

