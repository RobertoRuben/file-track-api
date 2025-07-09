from datetime import datetime
from fastapi import APIRouter, Depends, Query, Security, Body, Response
from src.app.core.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.dto.request import HamletRequestDTO
from src.app.dto.response import HamletResponseDTO, HamletPage, CurrentUserResponseDTO
from src.app.core.schema import MessageResponse
from src.app.service.interfaces import IHamletService
from src.app.service.dependencies import get_hamlet_service, get_current_user
from src.app.core.security.auth import Scopes

router = APIRouter(prefix="/hamlets", tags=["Hamlets"])

hamlet_tags_metadata = {
    "name": "Hamlets",
    "description": "Comprehensive rural settlement management system providing detailed geographical organization "
    "for small population centers and administrative subdivisions within larger territorial structures. Manages "
    "hamlet registrations, territorial relationships, and geographical hierarchies supporting governmental "
    "administration, demographic tracking, and regional planning initiatives. Facilitates rural community "
    "management, resource allocation, and administrative coordination for effective territorial governance.",
}


@router.post(
    "",
    response_model=HamletResponseDTO,
    summary="Create a new hamlet",
    status_code=201,
    responses={
        201: {
            "model": HamletResponseDTO,
            "description": "Hamlet created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {"model": ConflictError, "description": "Hamlet already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Establishes new rural settlement registrations with geographical validation and territorial "
    "hierarchy integration for comprehensive administrative management. Creates detailed hamlet profiles with "
    "unique naming requirements, settlement associations, and administrative boundaries supporting governmental "
    "territorial organization, demographic tracking, and regional development planning in rural administrative "
    "systems and geographical information management workflows.",
)
async def create_hamlet(
    hamlet_request: HamletRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_CREATE]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletResponseDTO:
    """
    Endpoint to create a new hamlet.

    This endpoint allows the creation of a new hamlet in the system. The hamlet data
    must be provided in the request body. If the hamlet is created successfully, a
    status code 201 is returned with the details of the created hamlet.

    :param hamlet_request: Request body containing the hamlet data.
    :param current_user: The user creating the hamlet, used for authorization.
    :param hamlet_service: Service that handles the hamlet creation logic.
    :return: The data of the created hamlet.
    """
    return await hamlet_service.add_hamlet(hamlet_request)


@router.get(
    "",
    response_model=list[HamletResponseDTO],
    summary="Get all hamlets",
    responses={
        200: {
            "model": list[HamletResponseDTO],
            "description": "List of hamlets",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive rural settlement inventory including all registered hamlets with geographical "
    "metadata, territorial relationships, and administrative details for complete territorial oversight. Provides "
    "enterprise-wide access to rural population center data supporting demographic analysis, resource planning, "
    "administrative coordination, and regional development initiatives requiring complete geographical information "
    "and territorial structure understanding.",
)
async def get_all_hamlets(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_READ]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> list[HamletResponseDTO]:
    """
    Endpoint to retrieve all hamlets.

    This endpoint returns a list of all available hamlets in the system. The response will include
    all hamlets stored in the database.

    :param current_user: The user requesting the hamlets, used for authorization.
    :param hamlet_service: Service to handle the query and retrieve all hamlets.
    :return: A list of hamlets in the system.
    """
    return await hamlet_service.get_all_hamlets()


@router.get(
    "/paginated",
    response_model=HamletPage,
    summary="Get hamlets with pagination",
    responses={
        200: {"model": HamletPage, "description": "Paginated list of hamlets"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Provides optimized paginated access to rural settlement collections for efficient large-scale "
    "geographical dataset management and enhanced administrative system performance. Implements server-side "
    "pagination with configurable page sizes to handle extensive territorial registries, reduce memory "
    "consumption, and improve user experience through controlled data loading. Essential for governmental "
    "systems managing extensive rural territories requiring responsive navigation capabilities.",
)
async def get_paginated_hamlets(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of hamlets per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_READ]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletPage:
    """
    Endpoint to retrieve hamlets in a paginated manner.

    This endpoint allows retrieving hamlets in a paginated format. The user can specify the page number
    and the number of hamlets per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of hamlets to return per page.
    :param current_user: The user requesting the paginated hamlets, used for authorization.
    :param hamlet_service: Service to handle the query and return paginated hamlets.
    :return: A paginated list of hamlets.
    """
    return await hamlet_service.get_hamlets_paginated(page, size)


@router.get(
    "/search",
    response_model=HamletPage,
    summary="Search hamlets by term",
    responses={
        200: {"model": HamletPage, "description": "Paginated list of hamlets"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes intelligent geographical search operations for precise rural settlement discovery and "
    "territorial location within comprehensive administrative systems. Implements fuzzy search capabilities "
    "with paginated results to efficiently locate specific hamlets within extensive geographical databases. "
    "Supports complex search scenarios including partial matches, case-insensitive queries, and geographical "
    "proximity searches for enhanced territorial navigation and administrative efficiency.",
)
async def find_hamlets(
    search_term: str | None = Query(None, description="Search term to filter hamlets"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of hamlets per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_READ]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletPage:
    """
    Endpoint to search hamlets using a search term.

    This endpoint allows searching for hamlets based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within hamlet names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user performing the search, used for authorization.
    :param hamlet_service: Service to handle the search logic and return results.
    :return: A paginated list of hamlets that match the search term.
    """
    return await hamlet_service.find(page, size, search_term)


@router.get(
    "/{hamlet_id}",
    response_model=HamletResponseDTO,
    summary="Get hamlet by ID",
    responses={
        200: {"model": HamletResponseDTO, "description": "Hamlet found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive hamlet profile and geographical metadata for specific rural settlements "
    "using unique administrative identifiers. Provides complete territorial information including settlement "
    "associations, administrative boundaries, and demographic details for detailed geographical analysis and "
    "administrative oversight. Essential for territorial verification workflows, geographical auditing, and "
    "rural development planning requiring precise settlement identification.",
)
async def get_hamlet_by_id(
    hamlet_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_READ]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletResponseDTO:
    """
    Endpoint to retrieve a hamlet by its ID.

    This endpoint retrieves the details of a specific hamlet identified by its ID. If the hamlet is found,
    the hamlet's data is returned. If not, a 404 error is returned.

    :param hamlet_id: The ID of the hamlet to retrieve.
    :param current_user: The user requesting the hamlet, used for authorization.
    :param hamlet_service: Service to handle the query and retrieve the hamlet.
    :return: The hamlet details.
    """
    return await hamlet_service.get_hamlet_by_id(hamlet_id)


@router.put(
    "/{hamlet_id}",
    response_model=HamletResponseDTO,
    summary="Update existing hamlet",
    responses={
        200: {
            "model": HamletResponseDTO,
            "description": "Hamlet updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        409: {"model": ConflictError, "description": "Hamlet name already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs comprehensive hamlet modification including name updates, territorial adjustments, and "
    "administrative metadata management with validation and geographical integrity preservation. Supports "
    "settlement evolution workflows while maintaining territorial consistency, enforcing naming uniqueness, "
    "and preserving hierarchical relationships. Enables dynamic geographical management through secure "
    "modification workflows with change tracking for administrative territorial oversight.",
)
async def update_hamlet(
    hamlet_id: int,
    hamlet_request: HamletRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_UPDATE]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletResponseDTO:
    """
    Endpoint to update an existing hamlet.

    This endpoint allows updating the details of an existing hamlet identified by its ID. If the hamlet
    is updated successfully, the updated hamlet data is returned. If the hamlet is not found,
    a 404 error is returned.

    :param hamlet_id: The ID of the hamlet to update.
    :param hamlet_request: The new data for the hamlet.
    :param current_user: The user updating the hamlet, used for authorization.
    :param hamlet_service: Service to handle the update logic.
    :return: The updated hamlet data.
    """
    return await hamlet_service.update_hamlet(hamlet_id, hamlet_request)


@router.delete(
    "/{hamlet_id}",
    response_model=MessageResponse,
    summary="Delete hamlet",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Hamlet deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes secure hamlet removal including dependency validation, territorial cascade handling, and "
    "geographical integrity preservation for complete administrative system management. Performs irreversible "
    "settlement elimination with comprehensive validation, hierarchical relationship checking, and territorial "
    "impact assessment to maintain system consistency. Implements governmental-grade deletion workflows with "
    "confirmation requirements and audit trail preservation for regulated territorial management. ⚠️ WARNING: "
    "This operation permanently removes the hamlet and may affect territorial relationships.",
)
async def delete_hamlet(
    hamlet_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_DELETE]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> MessageResponse:
    """
    Endpoint to delete a hamlet.

    This endpoint allows deleting a specific hamlet identified by its ID. If the hamlet is deleted
    successfully, a success message is returned. If the hamlet is not found, a 404 error is returned.

    :param hamlet_id: The ID of the hamlet to delete.
    :param current_user: The user deleting the hamlet, used for authorization.
    :param hamlet_service: Service to handle the delete logic.
    :return: A success message indicating that the hamlet has been deleted.
    """
    return await hamlet_service.delete_hamlet(hamlet_id)


@router.delete(
    "/bulk",
    response_model=MessageResponse,
    summary="Delete multiple hamlets by IDs",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Hamlets deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs bulk deletion of multiple hamlets in a single optimized operation. "
    "Validates each hamlet for dependencies and active relationships before removal. "
    "Implements transactional processing to ensure territorial integrity and provides "
    "detailed feedback on operation success. Critical operation requiring elevated permissions.",
)
async def delete_hamlets_bulk(
    hamlet_ids: list[int] = Body(..., description="List of hamlet IDs to delete"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_DELETE]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> MessageResponse:
    """
    Executes bulk deletion of multiple hamlets.

    This endpoint enables efficient removal of multiple hamlets through a single
    transactional operation. Performs comprehensive validation for each hamlet
    to ensure no active territorial dependencies exist before proceeding with deletion.
    Maintains geographical integrity throughout the bulk operation process.

    :param hamlet_ids: List of unique identifiers for hamlets to delete
    :param current_user: Authenticated user with bulk deletion privileges
    :param hamlet_service: Service layer handling bulk deletion logic
    :return: Operation summary with deletion results and any warnings
    """
    return await hamlet_service.delete_hamlets_by_ids(hamlet_ids)


@router.post(
    "/export-excel",
    response_class=Response,
    summary="Export hamlets to Excel",
    responses={
        200: {"description": "Excel file containing the requested hamlets"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "No hamlets found to export"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates comprehensive Excel reports containing detailed hamlet information for specified rural settlements. "
    "Creates professionally formatted spreadsheets with complete hamlet data including names, settlement relationships, "
    "and territorial metadata. Ideal for geographical reporting, territorial analysis, compliance documentation, "
    "and external reporting requirements. Supports bulk export with optimized file generation.",
)
async def export_hamlets_to_excel(
    hamlet_ids: list[int] = Body(..., description="List of hamlet IDs to export"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_READ]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> Response:
    """
    Generates comprehensive Excel reports for selected hamlets.

    This endpoint creates professionally formatted Excel spreadsheets containing
    detailed hamlet information for reporting, analysis, and compliance purposes.
    The generated files include complete hamlet metadata, settlement relationships,
    and formatting optimized for business use and external sharing.

    :param hamlet_ids: List of unique identifiers for hamlets to include in export
    :param current_user: Authenticated user with hamlet export privileges
    :param hamlet_service: Service layer handling Excel generation logic
    :return: Excel file as downloadable response with appropriate headers
    """
    excel_data = await hamlet_service.export_hamlets_to_excel(hamlet_ids)

    current_datetime = datetime.now().strftime("%d%m%Y%H%M")
    filename = f"hamlets_{current_datetime}.xlsx"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    return Response(content=excel_data, headers=headers)
