from .document_category_dependency import get_document_category_repository
from .document_repository_dependency import get_document_repository
from .documentary_topic_repository_dependency import get_documentary_topic_repository

__all__ = [
    "get_document_repository",
    "get_document_category_repository",
    "get_documentary_topic_repository",
]
