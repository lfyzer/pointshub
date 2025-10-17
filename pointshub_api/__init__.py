"""PointsHub Steam Points API Client.

A Python client library for interacting with the PointsHub Steam Points API.
Provides simple and intuitive methods for checking prices, buying Steam Points,
and managing account balance.

Modules:
    client: Main client class for API interactions
    errors: Custom exception classes for API errors
    models: Pydantic models for request/response data
    endpoints: Endpoint handlers for different API operations
"""

from .client import PointsHubClient
from .errors import (
    APIAuthenticationError,
    APIClientError,
    APIConnectionError,
    APIError,
    APIServerError,
    APITimeoutError,
)
from .models import (
    BuyOrder,
    GetBalance
)

__all__ = [
    "PointsHubClient",
    "APIError",
    "APIConnectionError",
    "APITimeoutError",
    "APIAuthenticationError",
    "APIServerError",
    "APIClientError",
    "GetPrice",
    "BuyOrder",
    "GetBalance",
]
