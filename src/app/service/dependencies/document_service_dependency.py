from fastapi import Depends
from src.app.service.interfaces import IDocumentService
from src.app.service.implementations import DocumentServiceImpl
from src.app.repository.interfaces import (
    IDocumentRepository,
    IDocumentCategoryRepository,
    ISubmitterRepository,
    IHamletRepository,
    ISettlementRepository,
    IDocumentaryTopicRepository,
)
from src.app.repository.dependencies import (
    get_document_repository,
    get_document_category_repository,
    get_submitter_repository,
    get_hamlet_repository,
    get_settlement_repository,
    get_documentary_topic_repository,
)


async def get_document_service(
    document_repository: IDocumentRepository = Depends(get_document_repository),
    document_category_repository: IDocumentCategoryRepository = Depends(
        get_document_category_repository
    ),
    submitter_repository: ISubmitterRepository = Depends(get_submitter_repository),
    hamlet_repository: IHamletRepository = Depends(get_hamlet_repository),
    settlement_repository: ISettlementRepository = Depends(get_settlement_repository),
    documentary_topic_repository: IDocumentaryTopicRepository = Depends(
        get_documentary_topic_repository
    ),
) -> IDocumentService:
    """
    Dependency function to get the document service implementation.

    This function creates and provides an instance of the document service
    implementation with all necessary repositories injected.

    :param document_repository: The document repository implementation
    :param document_category_repository: The document category repository implementation
    :param submitter_repository: The submitter repository implementation
    :param hamlet_repository: The hamlet repository implementation
    :param settlement_repository: The settlement repository implementation
    :param documentary_topic_repository: The documentary topic repository implementation
    :return: An implementation of IDocumentService configured with the provided repositories
    """
    return DocumentServiceImpl(
        document_repository=document_repository,
        document_category_repository=document_category_repository,
        submitter_repository=submitter_repository,
        hamlet_repository=hamlet_repository,
        settlement_repository=settlement_repository,
        documentary_topic_repository=documentary_topic_repository,
    )
