from .category_document_dependency import get_category_document_service
from .role_service_dependency import get_role_service
from .department_service_dependency import get_department_service

__all__ = [
    "get_category_document_service",
    "get_role_service",
    "get_department_service",
]