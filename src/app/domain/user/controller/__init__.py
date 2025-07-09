from .auth_controller import router as auth_router
from .role_controller import router as role_router

__all__ = [
    "auth_router",
    "role_router",
]
