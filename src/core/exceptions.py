from fastapi import HTTPException
from starlette import status


class UserDontHavePermissionsException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
