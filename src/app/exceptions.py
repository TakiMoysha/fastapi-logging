from fastapi.exceptions import HTTPException


class BaseAppException(Exception):
    pass


# =================================================================


class BaseHTTPException(HTTPException):
    pass
