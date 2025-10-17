"""Steam Points API models."""

from pydantic import BaseModel, validator

from ..enums import SteamPointsConstants


class GetBalance(BaseModel):
    """Get user account balance.

    Attributes:
        api_key: Unique API key for the user.
    """

    api_key: str


class BuyOrder(BaseModel):
    """Create a Steam Points buy order.

    Attributes:
        api_key: Unique API key for the user.
        puan: Points to buy (min 100, must be multiple of 100).
            Non-multiples are rounded down (e.g., 1999 → 1900).
        steam_link: Steam profile link with "https://" or Steam64ID.
    """

    api_key: str
    puan: int
    steam_link: str

    @validator("puan")
    def validate_puan_multiple(cls, v):
        if v < SteamPointsConstants.MIN_POINTS:
            raise ValueError(
                f"Points must be at least "
                f"{SteamPointsConstants.MIN_POINTS}"
            )
        if v % SteamPointsConstants.POINT_MULTIPLE != 0:
            raise ValueError(
                f"Points must be a multiple of "
                f"{SteamPointsConstants.POINT_MULTIPLE}"
            )
        return v

    @validator("steam_link")
    def validate_steam_link(cls, v):
        # Steam64ID format
        if v.startswith("https://"):
            return v
        elif v.startswith("7656") and len(v) == 17 and v.isdigit():
            return v
        else:
            raise ValueError(
                "Steam link must be a URL starting with https:// or a valid "
                "Steam64ID"
            )