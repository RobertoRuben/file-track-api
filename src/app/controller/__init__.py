from .document_category_controller import (
    router as document_category_router,
    document_category_tags_metadata,
)
from .role_controller import router as role_router, role_tags_metadata
from .department_controller import router as department_router, department_tags_metadata
from .documentary_topic_controller import (
    router as documentary_topic_router,
    documentary_topic_tags_metadata,
)
from .settlement_controller import router as settlement_router, settlement_tags_metadata
from .submitter_controller import router as submitter_router, submitter_tags_metadata
from .position_controller import router as position_router, position_tags_metadata
from .employee_controller import router as employee_router, employee_tags_metadata
from .hamlet_controller import router as hamlet_router, hamlet_tags_metadata
from .department_connection_controller import (
    router as department_connection_router,
    department_connection_tags_metadata,
)
from .user_controller import router as user_router, user_tags_metadata

__all__ = [
    "document_category_router",
    "document_category_tags_metadata",
    "role_router",
    "role_tags_metadata",
    "department_router",
    "department_tags_metadata",
    "documentary_topic_router",
    "documentary_topic_tags_metadata",
    "settlement_router",
    "settlement_tags_metadata",
    "submitter_router",
    "submitter_tags_metadata",
    "position_router",
    "position_tags_metadata",
    "employee_router",
    "employee_tags_metadata",
    "hamlet_router",
    "hamlet_tags_metadata",
    "department_connection_router",
    "department_connection_tags_metadata",
    "user_router",
    "user_tags_metadata",
]
