from sqlmodel import Field, Relationship
from typing import Annotated, TYPE_CHECKING, List
from schemas.product_schemas import ProductBase

if TYPE_CHECKING:
    from db.models.user_models import Users


class Products(ProductBase, table=True):
    id: Annotated[int, Field(primary_key=True)]
    seller_id: Annotated[int, Field(foreign_key="users.id")]
    seller: "Users" = Relationship(back_populates="products")
