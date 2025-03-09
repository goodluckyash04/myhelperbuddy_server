import uuid
from fastapi import Request
from app.core.logging_config import logger
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar

# Context variable to store request-specific logger
request_context_logger: ContextVar = ContextVar("request_context_logger", default=logger)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        request_uuid = str(uuid.uuid4())

        # Extract client IP
        forwarded_for = request.headers.get("X-Forwarded-For")
        real_ip = request.headers.get("X-Real-IP")

        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        elif real_ip:
            client_ip = real_ip
        else:
            client_ip = request.client.host  # Default to direct connection IP

        # Extract headers and MAC address
        headers = {k: v for k, v in request.headers.items() if k in ["user-agent", "content-type", "accept"]}
        mac_address = request.headers.get("X-MAC-Address", "0.0.0.0")
        request.state.request_uuid = request_uuid

        with logger.contextualize(request_id=request_uuid, ip=client_ip, mac=mac_address, url=request.url, header=headers):
            logger.info("Incoming Request")

            # Process the request
            response = await call_next(request)

            logger.info(f"Response status : {response.status_code}")

            return response
