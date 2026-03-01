from typing import Annotated, List
from pydantic import field_validator
from sqlmodel import SQLModel, Field
from app.core.enums import RolesEnum


class UserBase(SQLModel):
    username: Annotated[str, Field(unique=True, index=True)]
    email: Annotated[str, Field(unique=True)]
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls,instance:str):
        if not instance.endswith("@gmail.com"):
            raise ValueError
        return instance


class UserRegister(UserBase):
    pass


class UserCreatedResponse(SQLModel):
    username: str
    email: str


class UserLoggedInResponse(UserCreatedResponse):
    roles: List[RolesEnum]
