from .department_controller import router as department_router, department_tags_metadata
from .department_connection_controller import (
    router as department_connection_router,
    department_connection_tags_metadata
)

__all__ = [
    "department_router",
    "department_tags_metadata",
    "department_connection_router",
    "department_connection_tags_metadata"
]
