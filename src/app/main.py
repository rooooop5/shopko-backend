from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from db.database_lifecycle import startup, cleanup
from app.router.auth_router import auth_router
from app.router.roles_router import roles_router
from exception_handlers.http.http_handler import http_exception_handler
from exception_handlers.database.database_handler import integrity_error_handler


@asynccontextmanager
async def life(app: FastAPI):
    startup()
    yield
    cleanup()


app = FastAPI(lifespan=life)


app.include_router(auth_router)
app.include_router(roles_router)
app.add_exception_handler(HTTPException, handler=http_exception_handler)
app.add_exception_handler(IntegrityError,handler=integrity_error_handler)