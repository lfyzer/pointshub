"""Steam Points related enumerations."""

from enum import IntEnum


class SteamPointsConstants(IntEnum):
    """Steam Points purchase constants.
    
    Attributes:
        MIN_POINTS: Minimum points that can be purchased
        POINT_MULTIPLE: Points must be multiple of this value
    """
    
    MIN_POINTS = 100
    POINT_MULTIPLE = 100