from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import IntegrityError
from fastapi.requests import Request
from exception_handlers.database_exception_handler.database_exceptions import database_error

def IntegrityErrorHandler(request:Request,exception:IntegrityError):
    exception_string=str(exception.orig)
    print(exception_string)
    for error,http_exception in database_error.items():
        if error in exception_string:
            raise http_exception
    
        