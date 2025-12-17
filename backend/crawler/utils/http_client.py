"""
Async HTTP client wrapper using httpx.

Provides a configured httpx client with retry logic and rate limiting.
"""

import asyncio
import logging
from typing import Any

import httpx

from ..thepaper.config import DEFAULT_HEADERS, MAX_RETRIES, REQUEST_DELAY, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class HttpClient:
    """
    Async HTTP client with retry and rate limiting support.
    """

    def __init__(
        self,
        headers: dict[str, str] | None = None,
        timeout: int = REQUEST_TIMEOUT,
        max_retries: int = MAX_RETRIES,
        request_delay: float = REQUEST_DELAY,
    ):
        self.headers = headers or DEFAULT_HEADERS.copy()
        self.timeout = timeout
        self.max_retries = max_retries
        self.request_delay = request_delay
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "HttpClient":
        """Enter async context."""
        self._client = httpx.AsyncClient(
            headers=self.headers,
            timeout=self.timeout,
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """
        Make GET request with retry logic.

        Args:
            url: URL to fetch
            **kwargs: Additional arguments to pass to httpx.get

        Returns:
            httpx.Response object

        Raises:
            httpx.HTTPError: If all retries fail
        """
        return await self._request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        """
        Make POST request with retry logic.

        Args:
            url: URL to post to
            **kwargs: Additional arguments to pass to httpx.post

        Returns:
            httpx.Response object

        Raises:
            httpx.HTTPError: If all retries fail
        """
        return await self._request("POST", url, **kwargs)

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Make request with retry logic.

        Args:
            method: HTTP method
            url: URL to request
            **kwargs: Additional arguments

        Returns:
            httpx.Response object
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")

        last_error: Exception | None = None

        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    # Exponential backoff
                    delay = self.request_delay * (2 ** (attempt - 1))
                    logger.debug(f"Retry {attempt}/{self.max_retries} after {delay}s")
                    await asyncio.sleep(delay)

                response = await self._client.request(method, url, **kwargs)
                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                last_error = e
                logger.warning(f"HTTP {e.response.status_code} for {url}: {e}")
                if e.response.status_code < 500:
                    # Don't retry client errors
                    raise
            except httpx.RequestError as e:
                last_error = e
                logger.warning(f"Request error for {url}: {e}")

        # All retries exhausted
        if last_error:
            raise last_error
        raise httpx.RequestError(f"Failed after {self.max_retries} retries")

    async def get_json(self, url: str, **kwargs) -> dict[str, Any]:
        """GET request and parse JSON response."""
        response = await self.get(url, **kwargs)
        return response.json()

    async def post_json(self, url: str, **kwargs) -> dict[str, Any]:
        """POST request and parse JSON response."""
        response = await self.post(url, **kwargs)
        return response.json()

