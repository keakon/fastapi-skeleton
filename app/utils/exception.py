
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


class HTTPError(Exception):
    def __init__(self, status_code: int, code: int = 1, msg: str = ''):
        self.status_code = status_code
        self.code = code
        self.msg = msg


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'code': 1, 'msg': str(exc.detail)}
    )


async def http_error_handler(request: Request, exc: HTTPError):
    return JSONResponse(
        status_code=exc.status_code,
        content={'code': exc.code, 'msg': exc.msg}
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={'code': 1, 'msg': exc.args[0][0]['msg']}
    )


async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'code': 1, 'msg': 'Internal Server Error'}
    )


credentials_exception = HTTPException(
    status_code=401,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)
