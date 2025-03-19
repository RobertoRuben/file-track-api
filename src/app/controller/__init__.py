from .category_document_controller import router as category_document_router, category_document_tags_metadata
from .role_controller import router as role_router, role_tags_metadata

__all__ = [
    "category_document_router",
    "category_document_tags_metadata",
    "role_router",
    "role_tags_metadata"
]