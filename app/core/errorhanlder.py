from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


def register_exception_handler(application: FastAPI):
    application.add_exception_handler(HTTPException, http_exception_hanlder)
    application.add_exception_handler(Exception, generic_exception_handler)


def backend_exception_handler(request: Request, exc: Exception):
    error = serializer_error_message(exc)

    return JSONResponse(
        status_code=getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
        content={**error},
    )


def http_exception_hanlder(request: Request, exc: Exception):
    return backend_exception_handler(request, exc)


def generic_exception_handler(request: Request, exc: Exception):
    return backend_exception_handler(request, exc)


def serializer_error_message(exc: Exception) -> dict:
    error = {
        "success": False,
        "error": {
            "user_message": getattr(exc, "user_message", None),
            "status_code": getattr(exc, "status_code", 500),
            "system_code": getattr(exc, "system_code", None),
            "system_message": getattr(exc, "system_message", None),
        },
    }
    return error
