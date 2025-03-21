from abc import ABC, abstractmethod
from src.app.model.entity import CentroPoblado
from src.app.schema import Page


class ISettlementRepository(ABC):

    @abstractmethod
    async def save(self, settlement: CentroPoblado) -> CentroPoblado:
        """
        Guarda una entidad centro poblado en la base de datos.

        Args:
            settlement: La entidad centro poblado a guardar

        Returns:
            El centro poblado guardado con datos actualizados
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[CentroPoblado]:
        """
        Recupera todas las entidades de centro poblado de la base de datos.

        Returns:
            Una lista que contiene todos los centros poblados
        """
        pass

    @abstractmethod
    async def delete(self, settlement_id: int) -> bool:
        """
        Elimina una entidad centro poblado de la base de datos por su ID.

        Args:
            settlement_id: El ID del centro poblado a eliminar

        Returns:
            True si el centro poblado fue eliminado exitosamente, False en caso contrario
        """
        pass

    @abstractmethod
    async def get_by_id(self, settlement_id: int) -> CentroPoblado:
        """
        Recupera una entidad centro poblado de la base de datos por su ID.

        Args:
            settlement_id: El ID del centro poblado a recuperar

        Returns:
            La entidad centro poblado encontrada
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Recupera una lista paginada de entidades centro poblado de la base de datos.

        Args:
            page: El número de página (comienza en 1)
            size: El tamaño de cada página

        Returns:
            Un objeto Page que contiene centros poblados e información de paginación
        """
        pass

    @abstractmethod
    async def find(
        self,
        page: int,
        size: int,
        search_dict: dict[str, str],
    ) -> Page:
        """
        Recupera una lista paginada de entidades centro poblado basada en criterios de búsqueda.

        Args:
            page: El número de página (comienza en 1)
            size: El tamaño de cada página
            search_dict: Diccionario que contiene parámetros de búsqueda

        Returns:
            Un objeto Page con centros poblados que coinciden con los criterios de búsqueda
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Verifica si existe una entidad centro poblado en la base de datos según criterios específicos.

        Args:
            **kwargs: Pares clave-valor que representan los criterios de búsqueda

        Returns:
            True si existe un centro poblado coincidente, False en caso contrario
        """
        pass
