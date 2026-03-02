from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request


def http_exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "exception": {"status_code": exception.status_code, "detail": exception.detail},
            "path": request.url.path,
        }
    )