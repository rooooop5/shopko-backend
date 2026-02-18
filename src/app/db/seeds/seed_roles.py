from sqlmodel import SQLModel, Field, Session,Relationship
from sqlalchemy.exc import IntegrityError
from enum import Enum
from typing import Annotated, List


class RolesEnum(str, Enum):
    MODERATOR = "moderator"
    SELLER = "seller"
    CUSTOMER = "customer"


class Roles(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    role: Annotated[str, Field(unique=True)]


def seed_roles(session: Session):

    for roles in RolesEnum:
        try:
            role_instance = Roles(role=roles.value)
            session.add(role_instance)
            session.commit()
        except IntegrityError:
            session.rollback()
