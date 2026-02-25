from fastapi import APIRouter
from fastapi import Depends
from app.auth.security import create_access_token,authenticate_user
auth_router=APIRouter(prefix="/auth")

@auth_router.get("/")
def msg():
    return "This is the first endpoint of this project."

@auth_router.post("/get")
def login():
    pass