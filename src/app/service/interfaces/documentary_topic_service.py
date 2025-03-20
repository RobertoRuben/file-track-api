from abc import ABC, abstractmethod
from src.app.dto.request import DocumentaryTopicRequestDTO
from src.app.dto.response import DocumentaryTopicResponseDTO, DocumentaryTopicPage
from src.app.schema import MessageResponse

class IDocumentaryTopicService(ABC):
    """
    Interfaz para operaciones del servicio de ámbitos documentales.
    Define el contrato para la lógica de negocio relacionada con ámbitos documentales.
    """

    @abstractmethod
    async def add_documentary_topic(self, documentary_topic_request: DocumentaryTopicRequestDTO) -> DocumentaryTopicResponseDTO:
        """
        Añade un nuevo ámbito documental.

        Args:
            documentary_topic_request: El DTO que contiene los detalles del ámbito documental.

        Returns:
            El ámbito documental creado como DocumentaryTopicResponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_documentary_topics(self) -> list[DocumentaryTopicResponseDTO]:
        """
        Recupera todos los ámbitos documentales.

        Returns:
            Una lista de objetos DocumentaryTopicResponseDTO que representan todos los ámbitos documentales.
        """
        pass

    @abstractmethod
    async def update_documentary_topic(self, documentary_topic_id: int, documentary_topic_request: DocumentaryTopicRequestDTO) -> DocumentaryTopicResponseDTO:
        """
        Actualiza un ámbito documental existente.

        Args:
            documentary_topic_id: El ID del ámbito documental a actualizar.
            documentary_topic_request: El DTO que contiene los detalles actualizados del ámbito documental.

        Returns:
            El ámbito documental actualizado como DocumentaryTopicResponseDTO.
        """
        pass

    @abstractmethod
    async def delete_documentary_topic(self, documentary_topic_id: int) -> MessageResponse:
        """
        Elimina un ámbito documental por su ID.

        Args:
            documentary_topic_id: El ID del ámbito documental a eliminar.

        Returns:
            Un MessageResponse indicando el resultado de la eliminación.
        """
        pass

    @abstractmethod
    async def get_documentary_topic_by_id(self, documentary_topic_id: int) -> DocumentaryTopicResponseDTO:
        """
        Recupera un ámbito documental por su ID.

        Args:
            documentary_topic_id: El ID del ámbito documental a recuperar.

        Returns:
            El ámbito documental como DocumentaryTopicResponseDTO.
        """
        pass

    @abstractmethod
    async def get_documentary_topics_paginated(self, page: int, size: int) -> DocumentaryTopicPage:
        """
        Recupera una lista paginada de ámbitos documentales.

        Args:
            page: El número de página a recuperar.
            size: El número de ámbitos documentales por página.

        Returns:
            Un objeto DocumentaryTopicPage que contiene los ámbitos documentales paginados.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> DocumentaryTopicPage:
        """
        Busca ámbitos documentales según criterios de búsqueda.

        Args:
            page: El número de página a recuperar.
            size: El número de ámbitos documentales por página.
            search_term: El término a buscar en los nombres de los ámbitos documentales.

        Returns:
            Un objeto DocumentaryTopicPage que contiene los ámbitos documentales que coinciden con los criterios de búsqueda.
        """
        pass