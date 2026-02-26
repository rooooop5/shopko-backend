from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException
from app.models.user_models import UserRegister, Users
from app.auth.password_utils import hash_password, verify_password


def login_endpoint():
    pass


def register_endpoint(user: UserRegister, session: Session):
    user.password = hash_password(user.password)
    db_user = Users(**user.model_dump())
    try:
        session.add(db_user)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists broski")
