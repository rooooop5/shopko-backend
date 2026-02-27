from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request
from app.db.startup import startup,cleanup
from app.router.auth_router import auth_router


@asynccontextmanager
async def life(app: FastAPI):
    startup()
    yield
    cleanup()


app = FastAPI(lifespan=life)


app.include_router(auth_router)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "exception": {"status_code": exception.status_code, "detail": exception.detail},
            "path": request.url.path,
        }
    )
