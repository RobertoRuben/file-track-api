from .categoria_documento_dependency import get_categoria_documento_repository
from .rol_repository_dependency import get_rol_repository
from .area_repository_dependency import get_area_repository
from .documentary_topic_repository_dependency import get_documentary_topic_repository
from .settlement_repository_dependency import get_settlement_repository
from .submitter_repository_dependency import get_submitter_repository
from .position_repository_dependency import get_position_repository
from .employee_repository_dependency import get_employee_repository
from .hamlet_repository_dependency import get_hamlet_repository
from .area_connection_repository_dependency import get_area_connection_repository
from .user_repository_dependency import get_user_repository

__all__ = [
    "get_categoria_documento_repository",
    "get_rol_repository",
    "get_area_repository",
    "get_documentary_topic_repository",
    "get_settlement_repository",
    "get_submitter_repository",
    "get_position_repository",
    "get_employee_repository",
    "get_hamlet_repository",
    "get_area_connection_repository",
    "get_user_repository",
]
