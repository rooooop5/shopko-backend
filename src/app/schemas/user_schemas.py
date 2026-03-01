from typing import Annotated, List
from sqlmodel import SQLModel, Field
from app.core.enums import RolesEnum


class UserBase(SQLModel):
    username: Annotated[str, Field(unique=True, index=True)]
    email: Annotated[str, Field(unique=True, regex=f"@gmail\.com$")]
    password: str


class UserRegister(UserBase):
    pass


class UserCreatedResponse(SQLModel):
    username: str
    email: str


class UserLoggedInResponse(UserCreatedResponse):
    roles: List[RolesEnum]
