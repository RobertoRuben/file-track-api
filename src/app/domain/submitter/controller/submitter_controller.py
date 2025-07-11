from fastapi import APIRouter, Body, Depends, Query, Security, Response, Request
from src.app.core.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.core.exception.decorator import controller_handle_exceptions
from src.app.core.security.auth.dependencies import get_current_user
from src.app.core.security.auth.model import CurrentUser
from src.app.core.security.auth.constants import Scopes
from src.app.core.schema import MessageResponse
from src.app.domain.submitter.dto.request import SubmitterRequestDTO
from src.app.domain.submitter.dto.response import (
    SubmitterResponseDTO,
    SubmitterPage,
)
from src.app.domain.submitter.service.interface import ISubmitterService
from src.app.domain.submitter.service.dependencies import get_submitter_service


router = APIRouter(prefix="/submitters", tags=["Submitters"])

submitter_tags_metadata = {
    "name": "Submitters",
    "description": "Comprehensive citizen and stakeholder management system providing detailed personal information "
    "handling and identity verification for document submission workflows. Manages submitter registrations, "
    "personal data validation, and identification tracking supporting governmental document processing, citizen "
    "services, and administrative coordination. Facilitates secure personal information management, identity "
    "verification processes, and stakeholder relationship management for effective governmental operations.",
}


@router.post(
    "",
    response_model=SubmitterResponseDTO,
    summary="Create a new submitter",
    status_code=201,
    responses={
        201: {
            "model": SubmitterResponseDTO,
            "description": "Submitter created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {"model": ConflictError, "description": "Submitter already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Establishes new citizen submitter registrations with comprehensive identity validation and personal "
    "data verification for secure document management workflows. Creates detailed personal profiles with unique "
    "identification requirements, contact information validation, and identity verification supporting governmental "
    "document processing, citizen services, and stakeholder management in administrative systems requiring "
    "secure personal information handling and identity authentication.",
)
@controller_handle_exceptions
async def create_submitter(
    request: Request,
    submitter_request: SubmitterRequestDTO,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_CREATE]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterResponseDTO:
    """
    Endpoint to create a new submitter.

    This endpoint allows the creation of a new submitter in the system. The submitter data
    must be provided in the request body. If the submitter is created successfully, a
    status code 201 is returned with the details of the created submitter.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param submitter_request: Request body containing the submitter data.
    :param current_user: The user creating the submitter, used for authorization.
    :param submitter_service: Service that handles the submitter creation logic.
    :return: The data of the created submitter.
    """
    return await submitter_service.add_submitter(submitter_request)


@router.get(
    "",
    response_model=list[SubmitterResponseDTO],
    summary="Get all submitters",
    responses={
        200: {
            "model": list[SubmitterResponseDTO],
            "description": "List of submitters",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive citizen submitter registry including all registered individuals with personal "
    "identification data, contact information, and administrative details for complete stakeholder oversight. "
    "Provides enterprise-wide access to submitter profiles supporting citizen services, document processing "
    "workflows, administrative coordination, and stakeholder relationship management requiring complete personal "
    "information access and identity verification capabilities for governmental operations.",
)
@controller_handle_exceptions
async def get_all_submitters(
    request: Request,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_READ]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> list[SubmitterResponseDTO]:
    """
    Endpoint to retrieve all submitters.

    This endpoint returns a list of all available submitters in the system. The response will include
    all submitters stored in the database.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param current_user: The user requesting the submitters, used for authorization.
    :param submitter_service: Service to handle the query and retrieve all submitters.
    :return: A list of submitters in the system.
    """
    return await submitter_service.get_all_submitters()


@router.get(
    "/paginated",
    response_model=SubmitterPage,
    summary="Get submitters with pagination",
    responses={
        200: {"model": SubmitterPage, "description": "Paginated list of submitters"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Provides optimized paginated access to citizen submitter collections for efficient large-scale "
    "personal data management and enhanced governmental system performance. Implements server-side pagination "
    "with configurable page sizes to handle extensive citizen registries, reduce memory consumption, and improve "
    "user experience through controlled data loading. Essential for governmental systems managing extensive "
    "citizen databases requiring responsive navigation and privacy-compliant data handling.",
)
@controller_handle_exceptions
async def get_paginated_submitters(
    request: Request,
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of submitters per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_READ]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterPage:
    """
    Endpoint to retrieve submitters in a paginated manner.

    This endpoint allows retrieving submitters in a paginated format. The user can specify the page number
    and the number of submitters per page to optimize the query and reduce data overload.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param page: The page number to retrieve.
    :param size: The number of submitters to return per page.
    :param current_user: The user requesting the submitters, used for authorization.
    :param submitter_service: Service to handle the query and return paginated submitters.
    :return: A paginated list of submitters.
    """
    return await submitter_service.get_submitters_paginated(page, size)


@router.get(
    "/search",
    response_model=SubmitterPage,
    summary="Search submitters by term",
    responses={
        200: {"model": SubmitterPage, "description": "Paginated list of submitters"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes intelligent citizen search operations across personal identification fields for precise "
    "submitter discovery and identity verification within comprehensive administrative systems. Implements secure "
    "search capabilities with paginated results across names, surnames, and identification numbers while "
    "maintaining privacy compliance. Supports complex search scenarios including partial matches and case-"
    "insensitive queries for enhanced citizen identification and administrative efficiency.",
)
@controller_handle_exceptions
async def find_submitters(
    request: Request,
    search_term: str | None = Query(
        None, description="Search term to filter submitters"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of submitters per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_READ]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterPage:
    """
    Endpoint to search submitters using a search term.

    This endpoint allows searching for submitters based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param search_term: A term to search within submitter names, surnames or DNI.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user requesting the search, used for authorization.
    :param submitter_service: Service to handle the search logic and return results.
    :return: A paginated list of submitters that match the search term.
    """
    return await submitter_service.find(page, size, search_term)


@router.delete(
    "/bulk",
    response_model=MessageResponse,
    summary="Delete multiple submitters by IDs",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Submitters deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs bulk deletion of multiple submitter records in a single atomic operation for efficient "
    "citizen data management. Validates all submitter IDs, maintains referential integrity, and provides "
    "comprehensive audit trails for mass administrative operations and data cleanup workflows.",
)
@controller_handle_exceptions
async def delete_submitters_bulk(
    request: Request,
    submitter_ids: list[int] = Body(
        ..., description="List of submitter IDs for bulk deletion operation"
    ),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_DELETE]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> MessageResponse:
    """
    Performs efficient bulk deletion of multiple submitter records in a single atomic operation.

    This endpoint enables mass submitter record deletion for administrative cleanup,
    data migration, or large-scale citizen data management operations. Implements comprehensive
    validation, maintains system integrity, and provides detailed audit trails for
    compliance and organizational record-keeping requirements.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param submitter_ids: List of unique submitter identifiers for bulk deletion
    :param current_user: Authenticated user with bulk submitter deletion privileges
    :param submitter_service: Service layer handling complex bulk deletion logic
    :return: Comprehensive operation summary with success counts and audit information
    """
    return await submitter_service.delete_submitters_by_ids(submitter_ids)


@router.post(
    "/export-excel",
    response_class=Response,
    summary="Export submitters to Excel",
    responses={
        200: {"description": "Archivo Excel con los presentadores solicitados"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "No se encontraron presentadores para exportar",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates comprehensive Excel reports of selected submitter records with complete citizen data "
    "for administrative analytics, compliance reporting, and external system integration. Provides formatted spreadsheets "
    "with professional layouts, complete submitter information, and optimized data structures for governmental analysis.",
)
@controller_handle_exceptions
async def export_submitters_to_excel(
    request: Request,
    submitter_ids: list[int] = Body(
        ..., description="List of submitter IDs for Excel export generation"
    ),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_READ]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> Response:
    """
    Generates comprehensive Excel reports of selected submitter records for administrative analysis.

    This endpoint creates professional Excel spreadsheets containing complete submitter
    data including personal information and citizen details. Optimized for administrative
    analytics, compliance reporting, external system integration, and strategic citizen
    data management initiatives.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param submitter_ids: List of submitter identifiers for selective data export
    :param current_user: Authenticated user with submitter read privileges for audit tracking
    :param submitter_service: Service layer handling Excel generation and data formatting
    :return: Excel file download response with formatted submitter data and professional layout
    """
    from datetime import datetime

    excel_data = await submitter_service.export_submitters_to_excel(submitter_ids)

    current_datetime = datetime.now().strftime("%d%m%Y%H%M")
    filename = f"submitters_{current_datetime}.xlsx"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    return Response(content=excel_data, headers=headers)


@router.get(
    "/{submitter_id}",
    response_model=SubmitterResponseDTO,
    summary="Get submitter by ID",
    responses={
        200: {"model": SubmitterResponseDTO, "description": "Submitter found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive submitter profile and personal identification metadata for specific citizens "
    "using unique system identifiers. Provides complete personal information including identification details, "
    "contact data, and administrative records for detailed citizen analysis and governmental oversight. Essential "
    "for identity verification workflows, citizen service provision, and administrative processes requiring "
    "precise personal identification and privacy-compliant data access.",
)
@controller_handle_exceptions
async def get_submitter_by_id(
    request: Request,
    submitter_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_READ]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterResponseDTO:
    """
    Endpoint to retrieve a submitter by its ID.

    This endpoint retrieves the details of a specific submitter identified by its ID. If the submitter is found,
    the submitter's data is returned. If not, a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param submitter_id: The ID of the submitter to retrieve
    :param current_user: The user requesting the submitter, used for authorization.
    :param submitter_service: Service to handle the query and retrieve the submitter
    :return: The details of the submitter with the specified ID
    """
    return await submitter_service.get_submitter_by_id(submitter_id)


@router.put(
    "/{submitter_id}",
    response_model=SubmitterResponseDTO,
    summary="Update existing submitter",
    responses={
        200: {
            "model": SubmitterResponseDTO,
            "description": "Submitter updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        409: {"model": ConflictError, "description": "Submitter DNI already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs comprehensive submitter modification including personal data updates, contact information "
    "changes, and identification validation with privacy compliance and data integrity preservation. Supports "
    "citizen profile evolution workflows while maintaining identification uniqueness, enforcing data validation "
    "rules, and preserving audit trails. Enables secure personal information management through controlled "
    "modification workflows with change tracking for governmental administrative oversight and privacy compliance.",
)
@controller_handle_exceptions
async def update_submitter(
    request: Request,
    submitter_id: int,
    submitter_request: SubmitterRequestDTO,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_UPDATE]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterResponseDTO:
    """
    Endpoint to update an existing submitter.

    This endpoint allows updating the details of an existing submitter identified by its ID. If the submitter
    is updated successfully, the updated submitter data is returned. If the submitter is not found,
    a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param submitter_id: The ID of the submitter to update.
    :param submitter_request: The new data for the submitter.
    :param current_user: The user updating the submitter, used for authorization.
    :param submitter_service: Service to handle the update logic.
    :return: The updated submitter data.
    """
    return await submitter_service.update_submitter(submitter_id, submitter_request)


@router.delete(
    "/{submitter_id}",
    response_model=MessageResponse,
    summary="Delete submitter",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Submitter deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes secure submitter removal including dependency validation, document association checking, "
    "and personal data privacy compliance for complete citizen data management. Performs irreversible submitter "
    "elimination with comprehensive validation, document relationship verification, and privacy-compliant data "
    "deletion to maintain system integrity. Implements governmental-grade deletion workflows with confirmation "
    "requirements and audit trail preservation for regulated personal data management. ⚠️ WARNING: This operation "
    "permanently removes the submitter and may affect document submissions.",
)
@controller_handle_exceptions
async def delete_submitter(
    request: Request,
    submitter_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_DELETE]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> MessageResponse:
    """
    Endpoint to delete a submitter.

    This endpoint allows deleting a specific submitter identified by its ID. If the submitter is deleted
    successfully, a success message is returned. If the submitter is not found, a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param submitter_id: The ID of the submitter to delete.
    :param current_user: The user deleting the submitter, used for authorization.
    :param submitter_service: Service to handle the delete logic.
    :return: A success message indicating that the submitter has been deleted.
    """
    return await submitter_service.delete_submitter(submitter_id)
