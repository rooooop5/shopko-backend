from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from db.database_lifecycle import startup, cleanup
from app.router.auth_router import auth_router
from exception_handlers.http_exception_handler.http_handler import http_exception_handler
from exception_handlers.database_exception_handler.database_handler import IntegrityErrorHandler


@asynccontextmanager
async def life(app: FastAPI):
    startup()
    yield
    cleanup()


app = FastAPI(lifespan=life)


app.include_router(auth_router)
app.add_exception_handler(HTTPException, handler=http_exception_handler)
app.add_exception_handler(IntegrityError,IntegrityErrorHandler)