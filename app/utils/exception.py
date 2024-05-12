from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .error_code import ErrorCode


class HTTPError(Exception):
    def __init__(self, status_code: int, code: int = 1, msg: str = '', headers=None):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.headers = headers


async def http_error_handler(request: Request, exc: HTTPError):
    return JSONResponse(status_code=exc.status_code, content={'code': exc.code, 'msg': exc.msg}, headers=exc.headers)


async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={'code': 1, 'msg': exc.args[0][0]['msg']})


async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={'code': ErrorCode.INTERNAL_SERVER_ERROR, 'msg': 'Internal Server Error'}
    )


def unauthorized_error(msg) -> HTTPError:
    return HTTPError(
        status_code=401,
        code=ErrorCode.UNAUTHORIZED,
        msg=msg,
        headers={'WWW-Authenticate': 'Bearer'},
    )


expired_token_error = unauthorized_error('Expired token')
invalid_token_error = unauthorized_error('Invalid token')
not_authenticated_error = unauthorized_error('Not authenticated')

forbidden_error = HTTPError(
    status_code=403,
    code=ErrorCode.FORBIDDEN,
    msg='Forbidden',
)

not_found_error = HTTPError(
    status_code=404,
    code=ErrorCode.NOT_FOUND,
    msg='Not Found',
)

internal_server_error = HTTPError(
    status_code=500,
    code=ErrorCode.INTERNAL_SERVER_ERROR,
    msg='Internal Server Error',
)
