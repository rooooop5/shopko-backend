from fastapi import APIRouter
from fastapi import Depends
from app.auth.security import create_access_token,authenticate_user
auth_router=APIRouter(prefix="/auth",tags=['auth'])

@auth_router.get("/")
def msg():
    return "This is the default route of the auth router."

@auth_router.post("/register")
def login():
    # login_endpoint()
    pass