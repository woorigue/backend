from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


def register_exception_handler(application: FastAPI):
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(Exception, generic_exception_handler)


def backend_exception_handler(exc: Exception):
    error = serializer_error_message(exc)

    return JSONResponse(
        content={**error},
    )


def http_exception_handler(_: Request, exc: Exception):
    return backend_exception_handler(exc)


def generic_exception_handler(_: Request, exc: Exception):
    return backend_exception_handler(exc)


def serializer_error_message(exc: Exception) -> dict:
    error = {
        "error_code": getattr(exc, "error_code", 999999),
        "error_detail": getattr(exc, "error_detail", None),
    }
    return error
