from .category_document_controller import (
    router as category_document_router,
    category_document_tags_metadata,
)
from .role_controller import router as role_router, role_tags_metadata
from .department_controller import router as department_router, department_tags_metadata
from .documentary_topic_controller import (
    router as documentary_topic_router,
    documentary_topic_tags_metadata,
)
from .settlement_controller import router as settlement_router, settlement_tags_metadata

__all__ = [
    "category_document_router",
    "category_document_tags_metadata",
    "role_router",
    "role_tags_metadata",
    "department_router",
    "department_tags_metadata",
    "documentary_topic_router",
    "documentary_topic_tags_metadata",
    "settlement_router",
    "settlement_tags_metadata",
]
