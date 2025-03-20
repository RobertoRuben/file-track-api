from .categoria_documento_dependency import get_categoria_documento_repository
from .rol_repository_dependency import get_rol_repository
from .area_repository_dependency import get_area_repository

__all__ = [
    "get_categoria_documento_repository",
    "get_rol_repository",
    "get_area_repository"
]