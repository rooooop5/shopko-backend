from fastapi import APIRouter

auth_router=APIRouter(prefix="/auth")

@auth_router.get("/")
def msg():
    return "This is the first endpoint of this project."