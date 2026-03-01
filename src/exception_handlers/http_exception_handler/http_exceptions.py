from fastapi.exceptions import HTTPException
from fastapi import status

bad_request_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad request")
credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
user_already_exists_exception = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")
email_already_taken_exception = HTTPException(status_code=status.HTTP_409_CONFLICT,detail="email already taken")
user_does_not_exist_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
role_not_allowed_exception=HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="role not allowed")
incorrect_password_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect password")