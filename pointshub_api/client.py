import asyncio
import logging
from typing import Any, Dict, Optional

import aiohttp
from aiohttp import ClientConnectionError, ClientTimeout

from .endpoints import SteamEndpoints
from .errors import (
    APIClientError,
    APIConnectionError,
    APIError,
    APIServerError,
    APITimeoutError,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
_logger = logging.getLogger(__name__)


class PointsHubClient:
    """Client for interacting with the PointsHub Steam Points API.

    This client handles API key authentication and provides access to Steam
    Points purchasing functionality through the PointsHub service. The API
    supports buying Steam Points with long operation timeouts due to potential
    supplier delays.

    The client is organized into functional endpoints:
        - steam: Steam Points operations (price checking, purchasing, balance)

    Attributes:
        base_url (str): The base URL for the API (default:
            https://api.buysteampoints.com).
        api_key (Optional[str]): Your unique API key for authentication.
        max_retries (int): Maximum number of retry attempts for failed
            requests.
        request_timeout (int): Timeout in seconds for API requests (default:
            30 minutes).
        session (Optional[aiohttp.ClientSession]): The aiohttp ClientSession
            for making requests.
        steam (SteamEndpoints): Steam Points operation endpoints.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.buysteampoints.com",
        max_retries: int = 3,
        request_timeout: int = 1800,
    ):
        """Initializes the PointsHubClient.

        Args:
            api_key (Optional[str]): Your unique API key from PointsHub.
            base_url (str): The base URL for the API. Should not need to
                change.
            max_retries (int): Maximum retry attempts for failed requests.
            request_timeout (int): Request timeout in seconds. Default is 1800
                (30 min) due to potentially long supplier processing times.
        """
        self.base_url = base_url
        self.api_key = api_key
        self._max_retries = max_retries
        self._request_timeout = request_timeout
        self.session: Optional[aiohttp.ClientSession] = None
        self._session_lock = asyncio.Lock()
        self.steam = SteamEndpoints(self)

    async def __aenter__(self):
        """Enters the async context manager.

        Returns:
            The client instance for use in async with statements.
        """
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exits the async context manager, cleaning up resources.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.
        """
        await self.close()

    async def close(self):
        """Closes the aiohttp session and cleans up resources.

        Call this when you're done with the client to properly clean up
        network connections. Not needed if using async context manager.
        """
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
            _logger.debug("Closed HTTP session")

    def _get_headers(self) -> Dict[str, str]:
        """Gets the HTTP headers for API requests.

        Returns:
            Dict[str, str]: Dictionary of headers for JSON requests.
        """
        return {"Content-Type": "application/json"}

    async def _ensure_session(self):
        """Ensures an active aiohttp session exists.

        Creates a new session if none exists or if the current one is closed.
        Thread-safe through async lock.
        """
        if not self.session or self.session.closed:
            async with self._session_lock:
                if not self.session or self.session.closed:
                    timeout = aiohttp.ClientTimeout(
                        total=self._request_timeout
                    )
                    self.session = aiohttp.ClientSession(
                        timeout=timeout,
                        raise_for_status=False,
                    )
                    _logger.debug("Created new HTTP session")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Performs a request with retry and error handling logic.

        This method handles connection errors, timeouts, and HTTP errors with
        automatic retry using exponential backoff. It properly maps API errors
        to custom exception types.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): API endpoint path (e.g., '/api/price').
            json_data (Optional[Dict]): Optional JSON payload for POST requests.

        Returns:
            Dict[str, Any]: Response JSON as a dictionary.

        Raises:
            APIConnectionError: If connection to the API fails.
            APITimeoutError: If the request times out.
            APIServerError: If server returns 5xx error.
            APIClientError: If client error occurs (4xx responses).
            APIError: For other unexpected errors.
        """
        url = f"{self.base_url}{endpoint}"
        await self._ensure_session()

        for attempt in range(self._max_retries):
            try:
                async with self.session.request(
                    method,
                    url,
                    json=json_data,
                    headers=self._get_headers(),
                ) as response:
                    result = await response.json()

                    if response.status >= 400:
                        error_msg = result.get('error', 'Unknown error')
                        if 400 <= response.status < 500:
                            raise APIClientError(
                                f"Client error: {response.status} {error_msg}"
                            )
                        else:
                            raise APIServerError(
                                f"Server error: {response.status} {error_msg}"
                            )

                    return result

            except (ClientConnectionError, ClientTimeout) as e:
                if attempt < self._max_retries - 1:
                    wait_time = 1 * (2 ** attempt)
                    await asyncio.sleep(wait_time)
                else:
                    error_class = (
                        APIConnectionError
                        if isinstance(e, ClientConnectionError)
                        else APITimeoutError
                    )
                    raise error_class(
                        f"Request failed after {self._max_retries} attempts."
                    ) from e

        raise APIError("Request failed after all retries.")

    def set_api_key(self, api_key: str) -> None:
        """Set the API key for authentication.

        Use this to set or update your API key after client initialization.
        The API key is required for buy and balance operations.

        Args:
            api_key (str): Your unique API key from PointsHub.
                Get yours via /profile in the bot or Profile menu.
        """
        self.api_key = api_key
