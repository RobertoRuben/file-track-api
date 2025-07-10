from .document_category_dependency import get_document_category_service
from src.app.domain.user.service.dependencies.role_service_dependency import (
    get_role_service,
)
from src.app.domain.department.service.dependencies.department_service_dependency import (
    get_department_service,
)
from .documentary_topic_service_dependency import get_documentary_topic_service
from src.app.domain.location.service.dependencies.settlement_service_dependency import (
    get_settlement_service,
)
from src.app.domain.submitter.service.dependencies.submitter_service_dependency import (
    get_submitter_service,
)
from src.app.domain.employee.service.dependencies.position_service_dependency import (
    get_position_service,
)
from src.app.domain.employee.service.dependencies.employee_service_dependency import (
    get_employee_service,
)
from src.app.domain.location.service.dependencies.hamlet_service_dependency import (
    get_hamlet_service,
)
from src.app.domain.department.service.dependencies.department_connection_service_dependency import (
    get_department_connection_service,
)
from src.app.domain.user.service.dependencies.user_service_dependency import (
    get_user_service,
)
from src.app.core.security.auth.dependencies.auth_service_dependency import (
    get_auth_service,
)
from .auth_current_user_dependency import get_current_user
from .auth_scope_dependency import requires_scopes
from .document_service_dependency import get_document_service
from .report_service_dependency import get_report_service

__all__ = [
    "get_document_category_service",
    "get_role_service",
    "get_department_service",
    "get_documentary_topic_service",
    "get_settlement_service",
    "get_submitter_service",
    "get_position_service",
    "get_employee_service",
    "get_hamlet_service",
    "get_department_connection_service",
    "get_user_service",
    "get_auth_service",
    "get_current_user",
    "requires_scopes",
    "get_document_service",
    "get_report_service",
]
