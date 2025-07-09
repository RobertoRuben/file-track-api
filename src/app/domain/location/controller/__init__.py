from .hamlet_controller import router as hamlet_router, hamlet_tags_metadata
from .settlement_controller import router as settlement_router, settlement_tags_metadata

__all__ = [
    "hamlet_router",
    "settlement_router",
    "hamlet_tags_metadata",
    "settlement_tags_metadata",
]
