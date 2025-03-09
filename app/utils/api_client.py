import httpx
from typing import Optional, Dict, Any

from app.core.logging_config import logger


class APIClient:
    """A reusable HTTP client for making API requests."""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None):
        """Perform a GET request."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                return {"error": "HTTP error occurred"}
            except httpx.RequestError as e:
                logger.error(f"Request error: {e}")
                return {"error": "Failed to connect to API"}

    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None):
        """Perform a POST request with optional JSON or form data."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(f"{self.base_url}{endpoint}", data=data, json=json, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                return {"error": "HTTP error occurred"}
            except httpx.RequestError as e:
                logger.error(f"Request error: {e}")
                return {"error": "Failed to connect to API"}
