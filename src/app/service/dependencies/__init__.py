from .category_document_dependency import get_category_document_service
from .role_service_dependency import get_role_service
from .department_service_dependency import get_department_service
from .documentary_topic_service_dependency import get_documentary_topic_service
from .settlement_service_dependency import get_settlement_service
from .submitter_service_dependency import get_submitter_service
from .position_service_dependency import get_position_service
from .employee_service_dependency import get_employee_service
from .hamlet_service_dependency import get_hamlet_service
from .area_connection_service_dependency import get_area_connection_service
from .user_service_dependency import get_user_service

__all__ = [
    "get_category_document_service",
    "get_role_service",
    "get_department_service",
    "get_documentary_topic_service",
    "get_settlement_service",
    "get_submitter_service",
    "get_position_service",
    "get_employee_service",
    "get_hamlet_service",
    "get_area_connection_service",
    "get_user_service",
]
