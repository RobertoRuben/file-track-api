from datetime import datetime
from fastapi import APIRouter, Depends, Query, Security, Body, Response, Request
from src.app.core.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.core.exception.decorator import controller_handle_exceptions
from src.app.core.security.auth.model import CurrentUser
from src.app.core.security.auth.dependencies import get_current_user
from src.app.core.security.auth.constants import Scopes
from src.app.core.schema import MessageResponse
from src.app.domain.location.dto.request import SettlementRequestDTO
from src.app.domain.location.dto.response import (
    SettlementResponseDTO,
    SettlementPage,
)
from src.app.domain.location.service.interface import ISettlementService
from src.app.domain.location.service.dependencies import get_settlement_service


router = APIRouter(prefix="/settlements", tags=["Settlements"])

settlement_tags_metadata = {
    "name": "Settlements",
    "description": "Comprehensive territorial settlement management system providing administrative control for "
    "population centers, municipal boundaries, and governmental subdivision organization. Manages settlement "
    "registrations, territorial hierarchies, and administrative relationships supporting governmental operations, "
    "demographic tracking, and regional planning initiatives. Facilitates municipal administration, resource "
    "allocation, and territorial governance for effective administrative coordination and regional development.",
}


@router.post(
    "",
    response_model=SettlementResponseDTO,
    summary="Create a new settlement",
    status_code=201,
    responses={
        201: {
            "model": SettlementResponseDTO,
            "description": "Settlement created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {"model": ConflictError, "description": "Settlement already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Establishes new territorial settlement registrations with comprehensive administrative validation "
    "and governmental hierarchy integration for municipal and regional management. Creates detailed settlement "
    "profiles with unique naming requirements, administrative boundaries, and territorial classifications "
    "supporting governmental territorial organization, demographic administration, and regional development "
    "planning in municipal administrative systems and territorial governance workflows.",
)
@controller_handle_exceptions
async def create_settlement(
    request: Request,
    settlement_request: SettlementRequestDTO,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SETTLEMENT_CREATE]
    ),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementResponseDTO:
    """
    Endpoint to create a new settlement.

    This endpoint allows the creation of a new settlement in the system. The settlement data
    must be provided in the request body. If the settlement is created successfully, a status code 201
    with the created settlement's details is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param settlement_request: Request body containing settlement data.
    :param current_user: The user creating the settlement, used for authorization.
    :param settlement_service: Service to handle the settlement creation logic.
    :return: The created settlement data.
    """
    return await settlement_service.add_settlement(settlement_request)


@router.get(
    "",
    response_model=list[SettlementResponseDTO],
    summary="Get all settlements",
    responses={
        200: {
            "model": list[SettlementResponseDTO],
            "description": "List of settlements",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive territorial settlement registry including all registered population centers "
    "with administrative metadata, municipal boundaries, and governmental details for complete territorial "
    "oversight. Provides enterprise-wide access to settlement data supporting demographic analysis, resource "
    "planning, administrative coordination, and regional development initiatives requiring complete territorial "
    "information and municipal structure understanding for governmental operations.",
)
@controller_handle_exceptions
async def get_all_settlements(
    request: Request,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SETTLEMENT_READ]
    ),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> list[SettlementResponseDTO]:
    """
    Endpoint to retrieve all settlements.

    This endpoint returns a list of all available settlements in the system. The response will include
    all settlements stored in the database.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param current_user: The user requesting the settlements, used for authorization.
    :param settlement_service: Service to handle the query and retrieve all settlements.
    :return: A list of settlements in the system.
    """
    return await settlement_service.get_all_settlements()


@router.get(
    "/paginated",
    response_model=SettlementPage,
    summary="Get settlements with pagination",
    responses={
        200: {"model": SettlementPage, "description": "Paginated list of settlements"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Provides optimized paginated access to territorial settlement collections for efficient large-scale "
    "administrative dataset management and enhanced governmental system performance. Implements server-side "
    "pagination with configurable page sizes to handle extensive municipal registries, reduce memory consumption, "
    "and improve user experience through controlled data loading. Essential for governmental systems managing "
    "extensive territorial databases requiring responsive navigation and administrative efficiency.",
)
@controller_handle_exceptions
async def get_paginated_settlements(
    request: Request,
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of settlements per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SETTLEMENT_READ]
    ),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementPage:
    """
    Endpoint to retrieve settlements in a paginated manner.

    This endpoint allows retrieving settlements in a paginated format. The user can specify the page number
    and the number of settlements per page to optimize the query and reduce data overload.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param page: The page number to retrieve.
    :param size: The number of settlements to return per page.
    :param current_user: The user requesting the settlements, used for authorization.
    :param settlement_service: Service to handle the query and return paginated settlements.
    :return: A paginated list of settlements.
    """
    return await settlement_service.get_settlements_paginated(page, size)


@router.get(
    "/search",
    response_model=SettlementPage,
    summary="Search settlements by term",
    responses={
        200: {"model": SettlementPage, "description": "Paginated list of settlements"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Settlement not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes intelligent territorial search operations for precise settlement discovery and municipal "
    "location within comprehensive administrative systems. Implements fuzzy search capabilities with paginated "
    "results to efficiently locate specific settlements within extensive governmental databases. Supports complex "
    "search scenarios including partial matches, case-insensitive queries, and territorial proximity searches "
    "for enhanced municipal navigation and administrative coordination efficiency.",
)
@controller_handle_exceptions
async def find_settlements(
    request: Request,
    search_term: str | None = Query(
        None, description="Search term to filter settlements"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of settlements per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SETTLEMENT_READ]
    ),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementPage:
    """
    Endpoint to search settlements using a search term.

    This endpoint allows searching for settlements based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param search_term: A term to search within settlement names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user requesting the settlements, used for authorization.
    :param settlement_service: Service to handle the search logic and return results.
    :return: A paginated list of settlements that match the search term.
    """
    return await settlement_service.find(page, size, search_term)


@router.delete(
    "/bulk",
    response_model=MessageResponse,
    summary="Delete multiple settlements",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Settlements deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "One or more settlements not found",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes bulk deletion of multiple territorial settlements in a single atomic transaction to maintain "
    "administrative data consistency and governmental system integrity. This endpoint accepts a collection of "
    "settlement identifiers and removes all corresponding territorial entities from the system simultaneously. "
    "The operation follows an all-or-nothing approach - if any settlement cannot be deleted due to constraints "
    "or territorial dependencies, the entire operation is rolled back to prevent partial deletions. Before "
    "execution, the system validates settlement existence, checks for administrative relationships, and verifies "
    "user permissions. This operation permanently affects territorial hierarchies and may impact existing "
    "administrative structures throughout the governmental system. ⚠️ WARNING: This operation permanently "
    "removes settlements and may affect territorial dependencies.",
)
@controller_handle_exceptions
async def delete_settlements_bulk(
    request: Request,
    settlement_ids: list[int] = Body(
        ..., description="List of settlement IDs to delete"
    ),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SETTLEMENT_DELETE]
    ),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> MessageResponse:
    """
    Endpoint to delete multiple settlements.

    This endpoint allows deleting multiple settlements identified by their IDs. If all settlements
    are deleted successfully, a success message is returned. If any settlement is not found, a 404 error
    is returned. The request body should contain a list of settlement IDs.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param settlement_ids: List of settlement IDs to delete.
    :param current_user: The user performing the bulk deletion, used for auditing and permissions.
    :param settlement_service: Service to handle the bulk delete logic.
    :return: A success message indicating that the settlements have been deleted.
    """
    return await settlement_service.delete_settlements_by_ids(settlement_ids)


@router.post(
    "/export-excel",
    summary="Export settlements to Excel",
    responses={
        200: {
            "description": "Excel file with settlements data",
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
                    "schema": {"type": "string", "format": "binary"},
                },
            },
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "One or more settlements not found",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates professionally formatted Excel spreadsheets containing comprehensive territorial settlement "
    "data for governmental reporting, administrative analysis, and regulatory compliance purposes. This endpoint "
    "creates optimized Excel files with properly structured columns, formatted headers, and enhanced styling for "
    "improved readability and official documentation. Users can specify particular settlements for targeted "
    "exports or export the complete territorial registry. The generated files include detailed settlement "
    "information such as names, administrative classifications, territorial boundaries, population data, "
    "creation dates, and modification timestamps. Files are automatically named with timestamps to ensure "
    "uniqueness and provide comprehensive audit trails. This functionality supports governmental data backup "
    "procedures, regulatory compliance reporting, territorial analysis, and stakeholder communication requirements.",
)
@controller_handle_exceptions
async def export_settlements_to_excel(
    request: Request,
    settlement_ids: list[int] = Body(
        ...,
        description="List of settlement IDs to export. If empty, exports all settlements",
    ),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SETTLEMENT_READ]
    ),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> Response:
    """
    Endpoint to export settlements to Excel format.

    This endpoint generates an Excel file containing settlement data. Users can specify which
    settlements to export by providing a list of IDs, or export all settlements if no IDs are provided.
    The Excel file includes proper formatting, headers, and is returned as a downloadable stream.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param settlement_ids: Optional list of settlement IDs to export. If None, exports all settlements.
    :param current_user: The user requesting the export, used for auditing and permissions.
    :param settlement_service: Service to handle the Excel export logic.
    :return: A StreamingResponse containing the Excel file for download.
    """
    excel_data = await settlement_service.export_settlements_to_excel(settlement_ids)

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{current_datetime}.xlsx"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    return Response(
        content=excel_data,
        headers=headers,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get(
    "/{settlement_id}",
    response_model=SettlementResponseDTO,
    summary="Get settlement by ID",
    responses={
        200: {"model": SettlementResponseDTO, "description": "Settlement found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Settlement not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive settlement profile and administrative metadata for specific territorial "
    "entities using unique governmental identifiers. Provides complete municipal information including "
    "administrative boundaries, population data, and territorial classifications for detailed settlement "
    "analysis and governmental oversight. Essential for territorial verification workflows, administrative "
    "auditing, and municipal development planning requiring precise settlement identification.",
)
@controller_handle_exceptions
async def get_settlement_by_id(
    request: Request,
    settlement_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SETTLEMENT_READ]
    ),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementResponseDTO:
    """
    Endpoint to retrieve a settlement by its ID.

    This endpoint retrieves the details of a specific settlement identified by its ID. If the settlement is found,
    the settlement's data is returned. If not, a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param settlement_id: The ID of the settlement to retrieve.
    :param current_user: The user requesting the settlement, used for authorization.
    :param settlement_service: Service to handle the query and retrieve the settlement.
    :return:  details.
    """
    return await settlement_service.get_settlement_by_id(settlement_id)


@router.put(
    "/{settlement_id}",
    response_model=SettlementResponseDTO,
    summary="Update existing settlement",
    responses={
        200: {
            "model": SettlementResponseDTO,
            "description": "Settlement updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Settlement not found"},
        409: {"model": ConflictError, "description": "Settlement name already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs comprehensive settlement modification including name updates, territorial adjustments, and "
    "administrative metadata management with validation and municipal integrity preservation. Supports settlement "
    "evolution workflows while maintaining territorial consistency, enforcing naming uniqueness, and preserving "
    "hierarchical relationships. Enables dynamic territorial management through secure modification workflows "
    "with change tracking for governmental administrative oversight and municipal development coordination.",
)
@controller_handle_exceptions
async def update_settlement(
    request: Request,
    settlement_id: int,
    settlement_request: SettlementRequestDTO,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SETTLEMENT_UPDATE]
    ),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementResponseDTO:
    """
    Endpoint to update an existing settlement.

    This endpoint allows updating the details of an existing settlement identified by its ID. If the settlement
    is updated successfully, the updated settlement data is returned. If the settlement is not found,
    a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param settlement_id: The ID of the settlement to update.
    :param settlement_request: The new data for the settlement.
    :param current_user: The user updating the settlement, used for authorization.
    :param settlement_service: Service to handle the update logic.
    :return: The updated settlement data.
    """
    return await settlement_service.update_settlement(settlement_id, settlement_request)


@router.delete(
    "/{settlement_id}",
    response_model=MessageResponse,
    summary="Delete settlement",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Settlement deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Settlement not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes secure settlement removal including dependency validation, territorial cascade handling, "
    "and administrative integrity preservation for complete governmental system management. Performs irreversible "
    "settlement elimination with comprehensive validation, hierarchical relationship checking, and territorial "
    "impact assessment to maintain system consistency. Implements governmental-grade deletion workflows with "
    "confirmation requirements and audit trail preservation for regulated territorial administration. ⚠️ WARNING: "
    "This operation permanently removes the settlement and may affect territorial hierarchies.",
)
@controller_handle_exceptions
async def delete_settlement(
    request: Request,
    settlement_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.SETTLEMENT_DELETE]
    ),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> MessageResponse:
    """
    Endpoint to delete a settlement.

    This endpoint allows deleting a specific settlement identified by its ID. If the settlement is deleted
    successfully, a success message is returned. If the settlement is not found, a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param settlement_id: The ID of the settlement to delete
    :param current_user: The user deleting the settlement, used for authorization
    :param settlement_service: Service to handle the delete logic
    :return: A success message indicating that the settlement has been deleted
    """
    return await settlement_service.delete_settlement(settlement_id)
