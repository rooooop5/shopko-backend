from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, List, TYPE_CHECKING
from app.models.enums import RolesEnum

if TYPE_CHECKING:
    from app.models.rbac_models import Roles


class UsersRoles(SQLModel, table=True):
    user: Annotated[int, Field(primary_key=True, foreign_key="users.id")]
    role: Annotated[int, Field(primary_key=True, foreign_key="roles.id")]


class UserBase(SQLModel):
    username: Annotated[str, Field(unique=True, index=True)]
    email: Annotated[str, Field(unique=True, regex=f"@gmail\.com$")]
    password: str


class Users(UserBase, table=True):
    id: Annotated[int, Field(primary_key=True)]
    roles: List["Roles"] = Relationship(back_populates="users", link_model=UsersRoles)


class UserRegister(UserBase):
    pass


class UserLogin(UserBase):
    pass


class UserCreatedResponse(SQLModel):
    username: str
    email: str

class UserLoggedInResponse(UserCreatedResponse):
    roles:List[RolesEnum]
