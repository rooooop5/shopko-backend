from fastapi import status


database_errors = {
    "ix_users_username": {"status_code": status.HTTP_409_CONFLICT, "detail": "user already exists"},
    "users_email_key": {"status_code": status.HTTP_409_CONFLICT, "detail": "email already taken"},
}
