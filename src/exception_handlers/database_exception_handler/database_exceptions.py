from exception_handlers.http_exception_handler.http_exceptions import (
    email_already_taken_exception,
    user_already_exists_exception
)

database_error = {"ix_users_username": user_already_exists_exception, "user_email_key": email_already_taken_exception}
