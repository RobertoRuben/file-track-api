from .document_category_repository import IDocumentCategoryRepository
from .role_repository import IRoleRepository
from src.app.domain.department.repository.interface.department_repository import (
    IDepartmentRepository,
)
from .documentary_topic_repository import IDocumentaryTopicRepository
from .settlement_repository import ISettlementRepository
from .submitter_repository import ISubmitterRepository
from .position_repository import IPositionRepository
from .employee_repository import IEmployeeRepository
from .hamlet_repository import IHamletRepository
from .department_connection_repository import IDepartmentConnectionRepository
from .user_repository import IUserRepository
from .document_repository import IDocumentRepository

__all__ = [
    "IDocumentCategoryRepository",
    "IRoleRepository",
    "IDepartmentRepository",
    "IDocumentaryTopicRepository",
    "ISettlementRepository",
    "ISubmitterRepository",
    "IPositionRepository",
    "IEmployeeRepository",
    "IHamletRepository",
    "IDepartmentConnectionRepository",
    "IUserRepository",
    "IDocumentRepository",
]
