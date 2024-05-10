import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.router import router
from app.utils.exception import (
    HTTPError,
    exception_handler,
    http_error_handler,
    http_exception_handler,
    validation_error_handler,
)
from app.utils.importer import auto_import

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)1.1s %(asctime)s %(pathname)s:%(lineno)d] %(message)s',
    datefmt='%y%m%d %H:%M:%S',
)

auto_import('app/controllers')

app = FastAPI()
app.include_router(router)
app.exception_handler(Exception)(exception_handler)
app.exception_handler(HTTPException)(http_exception_handler)
app.exception_handler(HTTPError)(http_error_handler)
app.exception_handler(RequestValidationError)(validation_error_handler)
