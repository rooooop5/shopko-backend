from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, TYPE_CHECKING
from db.models.user_models import UsersRoles

if TYPE_CHECKING:
    from db.models.user_models import Users


class RolePermissions(SQLModel, table=True):
    role: Annotated[int, Field(foreign_key="roles.id", primary_key=True)]
    permission: Annotated[int, Field(foreign_key="permissions.id", primary_key=True)]


class Permissions(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    permission: Annotated[str, Field(unique=True)]
    roles: list["Roles"] = Relationship(back_populates="permissions", link_model=RolePermissions)


class Roles(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    role: Annotated[str, Field(unique=True)]
    permissions: list["Permissions"] = Relationship(back_populates="roles", link_model=RolePermissions)
    users: list["Users"] = Relationship(back_populates="roles", link_model=UsersRoles)
