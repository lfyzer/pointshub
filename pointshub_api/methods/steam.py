"""Steam Points operations - price checking, purchasing, balance management."""

from typing import Any, Dict

from ..models.steam import BuyOrder, GetBalance


class SteamMethods:
    """Handle Steam Points operations including price checking, purchasing, and
    balance management.

    This class provides methods to interact with the PointsHub Steam Points
    API. All purchasing and balance operations require a valid API key.
    """

    BASE_PATH = "/api"

    @staticmethod
    def get_endpoints() -> Dict[str, str]:
        """Get API endpoint URLs for Steam Points operations.

        Returns:
            Dict[str, str]: Dictionary mapping operation names to their
                endpoint URLs.
        """
        return {
            "price": f"{SteamMethods.BASE_PATH}/price",
            "buy": f"{SteamMethods.BASE_PATH}/buy",
            "balance": f"{SteamMethods.BASE_PATH}/balance"
        }

    def __init__(self, client):
        """Initialize with client reference.

        Args:
            client: Main PointsHubClient instance for making API requests.
        """
        self._client = client

    async def get_price(self) -> Dict[str, Any]:
        """Get current Steam Points price per point.

        This operation doesn't require an API key and can be called anonymously.

        Returns:
            Dict[str, Any]: Response containing current price information.

        Raises:
            APIError: If the request fails or returns an error.
        """
        return await self._client._make_request(
            "GET",
            self.get_endpoints()["price"]
        )

    async def buy(self, puan: int, steam_link: str) -> Dict[str, Any]:
        """Buy Steam Points for a specific Steam account.

        This operation requires a valid API key and can take up to 30 minutes
        to complete due to potential supplier processing delays.

        Args:
            puan (int): Number of Steam Points to buy. Must be at least 100
                and a multiple of 100. If points are not a multiple of 100,
                they are rounded down (e.g., 1999 → 1900). Minimum is 100.
            steam_link (str): Target Steam account. Can be either:
                - Full Steam profile URL starting with https://
                - Pure Steam64ID (76561199XXXXXXXXX format)
                Plain text without https:// that is not a Steam64ID will be
                rejected.

        Returns:
            Dict[str, Any]: Response containing purchase details.

        Raises:
            ValueError: If API key is not set.
            APIClientError: If insufficient balance, invalid Steam profile, or
                maintenance mode.
            APIError: For other API errors.
        """
        if not self._client.api_key:
            raise ValueError("API key is required for buy operations")

        order_data = BuyOrder(
            api_key=self._client.api_key,
            puan=puan,
            steam_link=steam_link
        )

        return await self._client._make_request(
            "POST",
            self.get_endpoints()["buy"],
            order_data.dict()
        )

    async def get_balance(self) -> Dict[str, Any]:
        """Get your current account balance.

        This operation requires a valid API key to check your account balance.

        Returns:
            Dict[str, Any]: Response containing balance information.

        Raises:
            ValueError: If API key is not set.
            APIClientError: If API key is invalid or other client errors.
            APIError: For other API errors.
        """
        if not self._client.api_key:
            raise ValueError("API key is required for balance operations")

        balance_data = GetBalance(api_key=self._client.api_key)

        return await self._client._make_request(
            "POST",
            self.get_endpoints()["balance"],
            balance_data.dict()
        )
    
