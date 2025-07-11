from .auth_controller import router as auth_router, auth_tags_metadata
from .role_controller import router as role_router, role_tags_metadata
from .user_controller import router as user_router, user_tags_metadata

__all__ = [
    "auth_router",
    "auth_tags_metadata",
    "role_router",
    "role_tags_metadata",
    "user_router",
    "user_tags_metadata",
]
