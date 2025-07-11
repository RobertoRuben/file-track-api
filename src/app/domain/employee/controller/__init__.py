from .employee_controller import router as employee_router, employee_tags_metadata
from .position_controller import router as position_router, position_tags_metadata

__all__ = [
    "employee_router",
    "position_router",
    "employee_tags_metadata",
    "position_tags_metadata",
]
