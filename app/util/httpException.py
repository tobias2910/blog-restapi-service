from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.requests import Request


class CustomException(HTTPException):
    pass


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler
    """
    return JSONResponse({'error': exc.detail}, status_code=exc.status_code)
