from typing import Optional, Any
from fastapi.responses import JSONResponse


class ResponseHandling:
    @staticmethod
    def success_response(
        status_code: int, message: str = "Success", data: Optional[Any] = None, meta: Optional[dict] = None
    ):
        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data or [],
                "metadata": meta or {}
            }
        )

    @staticmethod
    def error_response(
        status_code: int, message: str = "Error", meta: Optional[dict] = None
    ):
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "metadata": meta or {}
            }
        )

    @staticmethod
    def internal_server_error():
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error!!!, please try again after some time",
            }
        )


response = ResponseHandling()