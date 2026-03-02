from sqlalchemy.exc import IntegrityError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from exception_handlers.database.database_exceptions import database_errors


def integrity_error_handler(request: Request, db_exception: IntegrityError):
    db_error=classify_integrity_error(exception=db_exception)
    return json_response(db_error,request)
    

def classify_integrity_error(exception:IntegrityError):
    exception_string=str(exception.orig)
    for db_error in database_errors.keys():
        if db_error in exception_string:
            return db_error

def json_response(db_error:str,request:Request):
    exception=database_errors.get(db_error)
    exception["path"]=request.url.path
    return JSONResponse(status_code=exception.get("status_code"),content=exception)