from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.models.user_models import UserRegister,UserLogin, Users
from app.auth.password_utils import hash_password, verify_password


def login_endpoint(user:UserLogin,session:Session):
    pass


def register_endpoint(user: UserRegister, session: Session):
    user.password = hash_password(user.password)
    db_user = Users(**user.model_dump())
    try:
        session.add(db_user)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
    session.refresh(db_user)
    return JSONResponse(content={"user_details":db_user.model_dump()})