from .document_category_controller import (
    router as document_category_router,
    document_category_tags_metadata,
)
from .document_controller import router as document_controller, document_tags_metadata
from .documentary_topic_controller import (
    router as documentary_topic_router,
    documentary_topic_tags_metadata,
)

__all__ = [
    "document_category_router",
    "document_category_tags_metadata",
    "document_controller",
    "document_tags_metadata",
    "documentary_topic_router",
    "documentary_topic_tags_metadata",
]
