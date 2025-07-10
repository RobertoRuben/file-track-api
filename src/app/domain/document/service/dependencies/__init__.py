from .document_category_dependency import get_document_category_service
from .document_service_dependency import get_document_service
from .documentary_topic_service_dependency import get_documentary_topic_service
from .report_service_dependency import get_report_service

__all__ = [
    "get_document_category_service",
    "get_document_service",
    "get_documentary_topic_service",
    "get_report_service",
]