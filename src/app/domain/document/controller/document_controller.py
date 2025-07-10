from io import BytesIO
from fastapi import APIRouter, Depends, Query, Security, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional
from src.app.core.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    ForbiddenError,
    UnauthorizedError,
)
from src.app.core.security.auth.constants import Scopes
from src.app.core.schema import MessageResponse
from src.app.core.security.auth.model import CurrentUser
from src.app.core.security.auth.dependencies import get_current_user
from src.app.domain.document.dto.request import DocumentRequestDTO
from src.app.domain.document.dto.response import DocumentResponseDTO, DocumentPage

from src.app.domain.document.service.interface import IDocumentService
from src.app.domain.document.service.dependencies import get_document_service


router = APIRouter(prefix="/documents", tags=["Documents"])

document_tags_metadata = {
    "name": "Documents",
    "description": "Comprehensive document management system providing complete lifecycle control for organizational "
    "document processing, storage, and retrieval. Handles advanced document operations including secure file "
    "upload, metadata management, multi-entity associations, intelligent search capabilities, and automated "
    "categorization. Supports complex document workflows with submitter tracking, geographical assignments, "
    "topic classification, and temporal filtering for efficient enterprise document administration and compliance.",
}


@router.post(
    "",
    response_model=DocumentResponseDTO,
    summary="Create a new document",
    status_code=201,
    responses={
        201: {
            "model": DocumentResponseDTO,
            "description": "Document created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Related entity not found"},
        409: {
            "model": ConflictError,
            "description": "Document with the same title already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates comprehensive document records with secure file upload, metadata validation, and multi-entity "
    "associations. Establishes complete document lifecycle management including submitter tracking, categorical "
    "classification, geographical assignments, and topic organization. Validates all relational dependencies "
    "and generates unique registration codes for enterprise document management workflows.",
)
async def create_document(
    title: str = Form(...),
    subject: str = Form(...),
    pages: int = Form(...),
    document: UploadFile = File(...),
    submitter_id: int = Form(...),
    document_category_id: int = Form(...),
    documentary_topic_id: int = Form(...),
    settlement_id: int = Form(...),
    hamlet_id: Optional[int] = Form(None),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CREATE]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> DocumentResponseDTO:
    """
    Endpoint to create a new document.

    This endpoint creates a new document with the provided details. The document file is uploaded and stored,
    and the document is associated with related entities such as submitter, category, documentary topic,
    hamlet, and settlement. The document is registered by the current user.

    :param title: The title of the document
    :param subject: The subject of the document
    :param pages: The number of pages in the document
    :param document: The document file to upload
    :param submitter_id: The ID of the submitter of the document
    :param document_category_id: The ID of the document's category
    :param documentary_topic_id: The ID of the documentary topic
    :param settlement_id: The ID of the settlement
    :param hamlet_id: The ID of the hamlet (optional)
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the document creation logic
    :return: The data of the created document
    """
    document_content = await document.read()

    document_request = DocumentRequestDTO(
        title=title,
        subject=subject,
        pages=pages,
        document=document_content,
        submitter_id=submitter_id,
        document_category_id=document_category_id,
        documentary_topic_id=documentary_topic_id,
        settlement_id=settlement_id,
        hamlet_id=hamlet_id,
    )

    return await document_service.add_document(document_request, current_user)


@router.get(
    "",
    response_model=list[DocumentResponseDTO],
    summary="Get all documents",
    responses={
        200: {
            "model": list[DocumentResponseDTO],
            "description": "List of documents",
        },
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete collection of all documents registered in the enterprise document "
    "management system with comprehensive metadata, relational associations, and workflow status information. "
    "Returns complete document profiles including submitter details, categorical classifications, geographical "
    "assignments, and temporal tracking for full enterprise document inventory management and audit trail purposes.",
)
async def get_all_documents(
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_READ]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> list[DocumentResponseDTO]:
    """
    Endpoint to retrieve all documents.

    This endpoint returns a list of all available documents in the system. The response will include
    all documents stored in the database with their complete details.

    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the query and retrieve all documents
    :return: A list of all documents in the system
    """
    return await document_service.get_all_documents()


@router.get(
    "/paginated",
    response_model=DocumentPage,
    summary="Get documents with pagination",
    responses={
        200: {
            "model": DocumentPage,
            "description": "Paginated list of documents",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "No documents found on the specified page",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Provides optimized paginated access to enterprise document collections for efficient large-scale "
    "dataset management and improved system performance. Implements server-side pagination with configurable page "
    "sizes to handle extensive document repositories, reduce memory consumption, and enhance user experience through "
    "controlled data loading. Essential for enterprise environments with high document volumes requiring responsive "
    "browsing capabilities and resource optimization.",
)
async def get_paginated_documents(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of documents per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_READ]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> DocumentPage:
    """
    Endpoint to retrieve documents in a paginated manner.

    This endpoint allows for retrieving documents in a paginated format. The user can specify the page
    number and the number of documents per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve
    :param size: The number of documents to return per page
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the query and return paginated documents
    :return: A paginated list of documents
    """
    return await document_service.get_documents_paginated(page, size)


@router.get(
    "/search",
    response_model=DocumentPage,
    summary="Search documents by term",
    responses={
        200: {
            "model": DocumentPage,
            "description": "Paginated list of matching documents",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "No documents found matching the search",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes intelligent multi-field document search across registration codes, titles, subjects, and "
    "submitter identification for comprehensive document discovery and retrieval. Implements fuzzy search capabilities "
    "with paginated results to efficiently locate documents within large enterprise repositories. Supports complex "
    "search scenarios including partial matches, case-insensitive queries, and cross-reference lookups for enhanced "
    "document accessibility and knowledge management workflows.",
)
async def search_documents(
    search: str = Query(..., description="Search term to filter documents"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of documents per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_READ]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> DocumentPage:
    """
    Endpoint to search documents using a search term.

    This endpoint allows searching for documents based on a given term. Results are returned in a
    paginated format, where the user can specify the page number and the number of results per page.
    The search covers registration code, title, subject, and submitter DNI fields.

    :param search: Term to search for in the document details
    :param page: The page number to retrieve
    :param size: The number of results per page
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the search logic and return the results
    :return: A paginated list of documents that match the search term
    """
    return await document_service.find(page, size, search)


@router.get(
    "/current-date",
    response_model=DocumentPage,
    summary="Get today's documents with pagination",
    responses={
        200: {
            "model": DocumentPage,
            "description": "Paginated list of documents created today",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "No documents found for today",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Provides real-time access to current day document registrations with temporal filtering for immediate "
    "workflow management and daily operations monitoring. Delivers paginated results of documents processed within "
    "the current business day, enabling efficient daily document tracking, workload assessment, and operational "
    "oversight. Essential for time-sensitive document processing workflows, daily reporting requirements, and "
    "administrative productivity analysis.",
)
async def get_documents_by_current_date(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of documents per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_READ]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> DocumentPage:
    """
    Endpoint to retrieve documents created on the current date in a paginated manner.

    This endpoint allows for retrieving documents that were created today. The results are
    presented in a paginated format, where the user can specify the page number and the
    number of documents per page.

    :param page: The page number to retrieve
    :param size: The number of documents to return per page
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the query and return today's documents
    :return: A paginated list of documents created today
    """
    return await document_service.get_documents_by_current_date(page, size)


@router.get(
    "/current-date/search",
    response_model=DocumentPage,
    summary="Search today's documents by term",
    responses={
        200: {
            "model": DocumentPage,
            "description": "Paginated list of today's matching documents",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "No documents found for today matching the search",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes targeted search operations within current day document registrations combining temporal "
    "filtering with intelligent search capabilities for precise daily document discovery. Performs multi-field "
    "searches across registration codes, titles, subjects, and submitter information within today's document "
    "entries, providing real-time search functionality for immediate document location and daily workflow "
    "optimization in time-critical enterprise environments.",
)
async def search_documents_by_current_date(
    search: str = Query(..., description="Search term to filter today's documents"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of documents per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_READ]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> DocumentPage:
    """
    Endpoint to search documents created on the current date using a search term.

    This endpoint allows searching for documents that were created today based on a given term.
    Results are returned in a paginated format, where the user can specify the page number
    and the number of results per page. The search covers registration code, title, subject,
    and submitter DNI fields.

    :param search: Term to search for in today's document details
    :param page: The page number to retrieve
    :param size: The number of results per page
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the search logic and return the results
    :return: A paginated list of today's documents that match the search term
    """
    return await document_service.find_by_current_date(page, size, search)


@router.get(
    "/{document_id}",
    response_model=DocumentResponseDTO,
    summary="Get document by ID",
    responses={
        200: {
            "model": DocumentResponseDTO,
            "description": "Document found",
        },
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Document not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive document profile and metadata for a specific document using its unique "
    "system identifier. Provides complete document information including content details, relational associations, "
    "workflow status, and audit trail information for detailed document inspection and verification purposes. "
    "Essential for document management workflows requiring precise document identification and complete "
    "administrative oversight.",
)
async def get_document_by_id(
    document_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_READ]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> DocumentResponseDTO:
    """
    Endpoint to retrieve a document by its ID.

    This endpoint retrieves the details of a specific document identified by its ID.
    If found, it returns the document data. If not, it returns a 404 error.

    :param document_id: ID of the document to retrieve
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the query and retrieve the document
    :return: Document details
    """
    return await document_service.get_document_by_id(document_id)


@router.put(
    "/{document_id}",
    response_model=DocumentResponseDTO,
    summary="Update existing document",
    responses={
        200: {
            "model": DocumentResponseDTO,
            "description": "Document updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "Document or related entity not found",
        },
        409: {
            "model": ConflictError,
            "description": "Document with the same title already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs comprehensive document modification including metadata updates, file replacement, and "
    "relational association changes with validation and audit trail maintenance. Supports partial or complete "
    "document updates while preserving data integrity, enforcing business rules, and maintaining version control. "
    "Enables document lifecycle management through secure modification workflows with rollback capabilities and "
    "change tracking for enterprise document administration and compliance requirements.",
)
async def update_document(
    document_id: int,
    title: str = Form(...),
    subject: str = Form(...),
    pages: int = Form(...),
    submitter_id: int = Form(...),
    document_category_id: int = Form(...),
    documentary_topic_id: int = Form(...),
    settlement_id: int = Form(...),
    hamlet_id: int | None = Form(default=None),
    document: UploadFile | None = File(default=None),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_UPDATE]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> DocumentResponseDTO:
    """
    Endpoint to update an existing document.

    This endpoint allows updating the details of an existing document identified by its ID.
    The document file can be replaced (optional), and the document's associations with other entities can be modified.
    If the document is updated successfully, it returns the updated data. If not found, it returns a 404 error.

    :param document_id: ID of the document to update
    :param title: The new title of the document
    :param subject: The new subject of the document
    :param pages: The new number of pages in the document
    :param submitter_id: The new ID of the submitter
    :param document_category_id: The new ID of the document's category
    :param documentary_topic_id: The new ID of the documentary topic
    :param settlement_id: The new ID of the settlement
    :param hamlet_id: The new ID of the hamlet (optional)
    :param document: The new document file to upload (optional)
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the update logic
    :return: Updated data of the document
    """
    document_content = None
    if document:
        document_content = await document.read()

    document_request = DocumentRequestDTO(
        title=title,
        subject=subject,
        pages=pages,
        document=document_content,
        submitter_id=submitter_id,
        document_category_id=document_category_id,
        documentary_topic_id=documentary_topic_id,
        settlement_id=settlement_id,
        hamlet_id=hamlet_id,
    )

    return await document_service.update_document(
        document_id, document_request, current_user.id
    )


@router.delete(
    "/{document_id}",
    response_model=MessageResponse,
    summary="Delete document by ID",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Document deleted successfully",
        },
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Document not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes secure document removal including file deletion, metadata cleanup, and audit trail "
    "preservation for complete document lifecycle management. Performs irreversible document elimination with "
    "comprehensive validation, dependency checking, and cascade deletion handling to maintain system integrity. "
    "Implements enterprise-grade deletion workflows with confirmation requirements, backup procedures, and "
    "compliance logging for regulated document management environments. ⚠️ WARNING: This operation is permanent "
    "and cannot be undone.",
)
async def delete_document(
    document_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_DELETE]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> MessageResponse:
    """
    Endpoint to delete a document.

    This endpoint allows deleting a specific document identified by its ID. If deleted successfully,
    it returns a success message. If not found, it returns a 404 error.

    :param document_id: ID of the document to delete
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the deletion logic
    :return: Success message indicating the document has been deleted
    """
    return await document_service.delete_document(document_id)


@router.get(
    "/download/{registration_code}",
    summary="Download document by registration code",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "Document file downloaded successfully",
        },
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Document not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Provides secure document file retrieval and streaming download functionality using unique "
    "registration codes for precise document access and distribution. Implements optimized file streaming with "
    "appropriate content headers, MIME type detection, and download metadata for seamless client integration. "
    "Supports enterprise document sharing workflows with access control validation, download tracking, and "
    "secure file transmission for regulated document distribution and stakeholder collaboration.",
)
async def download_document_by_registration_code(
    registration_code: str,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_READ]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> StreamingResponse:
    """
    Endpoint to download a document by its registration code.

    This endpoint retrieves a document file by its registration code and streams it as a download.
    The file is returned with appropriate headers to trigger a download in the client's browser.

    :param registration_code: Registration code of the document to download
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the document retrieval
    :return: A streaming response containing the document file
    """
    content, _, content_type = await document_service.get_document_by_registration_code(
        registration_code
    )

    extension = "pdf"
    if content_type:
        if content_type == "application/pdf":
            extension = "pdf"

    content_stream = BytesIO(content)

    response = StreamingResponse(content_stream, media_type=content_type)
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{registration_code}.{extension}"'
    )
    response.headers["Content-Length"] = str(len(content))

    return response


@router.get(
    "/{document_id}/information",
    response_model=DocumentResponseDTO,
    summary="Get detailed document information by ID",
    responses={
        200: {
            "model": DocumentResponseDTO,
            "description": "Detailed document information found",
        },
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Document not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Delivers comprehensive document intelligence including enriched metadata, complete relational "
    "context, and administrative details for advanced document analysis and management oversight. Provides "
    "detailed document profiles with expanded categorical information, geographical assignments, submitter "
    "profiles, and topic classifications for thorough document understanding and enterprise-level document "
    "intelligence workflows requiring complete contextual information.",
)
async def get_document_information_by_id(
    document_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_READ]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> DocumentResponseDTO:
    """
    Endpoint to retrieve detailed information about a document by its ID.

    This endpoint returns comprehensive information about a document, including
    related entities details such as documentary topic name, document category name,
    settlement name, hamlet name, and submitter information.

    :param document_id: ID of the document to retrieve detailed information for
    :param current_user: The user making the request, used for authorization
    :param document_service: Service to handle the query and retrieve the document information
    :return: Detailed document information
    """
    return await document_service.get_document_information_by_id(document_id)


@router.get(
    "/{document_id}/report",
    summary="Generate document registration report",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "Report generated successfully",
        },
        401: {"model": UnauthorizedError, "description": "Unauthorized"},
        403: {"model": ForbiddenError, "description": "Forbidden"},
        404: {"model": NotFoundError, "description": "Document not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Generates comprehensive PDF registration reports containing complete document profiles, metadata "
    "summaries, and administrative details for compliance documentation and audit trail purposes. Creates "
    "professional-grade reports with standardized formatting, institutional branding, and regulatory compliance "
    "information for official document certification, administrative verification, and enterprise reporting "
    "requirements in formal business and legal contexts.",
)
async def generate_document_report(
    document_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_READ]
    ),
    document_service: IDocumentService = Depends(get_document_service),
) -> StreamingResponse:
    """
    Endpoint to generate and download a detailed PDF report for a specific document.

    This endpoint creates a comprehensive PDF report for a given document,
    including registration details, metadata, and related entities.

    :param document_id: ID of the document to generate the report for
    :param current_user: The user making the request, used for authorization
    :param document_service: Service responsible for generating the report
    :return: A StreamingResponse containing the PDF file
    """
    content, filename = await document_service.generate_document_registration_report(
        document_id
    )

    if not isinstance(content, bytes):
        content = await content

    content_stream = BytesIO(content)
    response = StreamingResponse(content_stream, media_type="application/pdf")
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    response.headers["Content-Length"] = str(len(content))

    return response
