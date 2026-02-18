from sqlmodel import SQLModel, Session, Field
from sqlalchemy.exc import IntegrityError
from typing import Annotated,List
from enum import Enum


class PermissionsEnum(Enum):
    viewProducts = "view_products"
    listProducts = "list_products"
    getProduct = "get_product"
    placeOrder = "place_order"
    cancelOrder = "cancel_order"
    listOwnOrders = "list_own_orders"
    viewOwnOrder = "view_own_order"



class Permissions(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    permission: Annotated[str, Field(unique=True)]


def seed_permissions(session: Session):
    for perm in PermissionsEnum:
        permission_instance = Permissions(permission=perm.value)
        try:
            session.add(permission_instance)
            session.commit()
        except IntegrityError:
            session.rollback()
