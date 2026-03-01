from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, List, TYPE_CHECKING
from app.schemas.user_schemas import UserBase

if TYPE_CHECKING:
    from app.models.rbac_models import Roles


class UsersRoles(SQLModel, table=True):
    user: Annotated[int, Field(primary_key=True, foreign_key="users.id")]
    role: Annotated[int, Field(primary_key=True, foreign_key="roles.id")]


class Users(UserBase, table=True):
    id: Annotated[int, Field(primary_key=True)]
    roles: List["Roles"] = Relationship(back_populates="users", link_model=UsersRoles)
