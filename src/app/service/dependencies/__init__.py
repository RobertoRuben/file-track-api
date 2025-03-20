from .category_document_dependency import get_category_document_service
from .role_service_dependency import get_role_service
from .department_service_dependency import get_department_service
from .documentary_topic_service_dependency import get_documentary_topic_service

__all__ = [
    "get_category_document_service",
    "get_role_service",
    "get_department_service",
    "get_documentary_topic_service",
]