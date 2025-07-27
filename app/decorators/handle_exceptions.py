# utils/decorators.py

from functools import wraps

from fastapi import HTTPException

from app.api.error_handlers import response
from app.core.logging_config import logger


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            logger.error(e.detail)
            return response.error_response(status_code=e.status_code, message=e.detail)
        except Exception as e:
            logger.critical(str(e))
            return response.internal_server_error()

    return wrapper
