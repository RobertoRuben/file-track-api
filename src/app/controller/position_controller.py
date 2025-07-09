from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    Query,
    Security,
    Body,
    Response,
)
from src.app.core.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.dto.request import PositionRequestDTO
from src.app.dto.response import (
    PositionResponseDTO,
    PositionPage,
    CurrentUserResponseDTO,
)
from src.app.core.schema import MessageResponse
from src.app.service.interfaces import IPositionService
from src.app.service.dependencies import get_position_service, get_current_user
from src.app.security.auth.constants import Scopes

router = APIRouter(prefix="/positions", tags=["Positions"])

position_tags_metadata = {
    "name": "Positions",
    "description": "Comprehensive enterprise job position management system facilitating organizational role definition, "
    "employee assignment coordination, and workforce structure administration for effective human resource "
    "operations. Manages complex job role hierarchies supporting HR workflows, career progression planning, "
    "and organizational development through structured position frameworks. Enables sophisticated workforce "
    "management with advanced search capabilities, bulk operations, and detailed audit trails supporting "
    "enterprise human resource governance, talent management, and organizational efficiency across complex "
    "employment structures and career development environments.",
}


@router.post(
    "",
    response_model=PositionResponseDTO,
    summary="Create a new position",
    status_code=201,
    responses={
        201: {
            "model": PositionResponseDTO,
            "description": "Position created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {"model": ConflictError, "description": "Position already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new job position in the organizational structure. Validates name uniqueness "
    "and establishes a new role definition that can be assigned to employees. Position names must "
    "be descriptive and follow organizational naming conventions to maintain clarity in HR management.",
)
async def create_position(
    position_request: PositionRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.POSITION_CREATE]
    ),
    position_service: IPositionService = Depends(get_position_service),
) -> PositionResponseDTO:
    """
    Creates a new job position in the organizational structure.

    This endpoint establishes a new position that defines a specific role within the organization.
    Positions serve as templates for employee assignments and help maintain organizational hierarchy.
    The system validates that position names are unique to prevent confusion in HR management.
    Created positions can immediately be assigned to employees and integrated into reporting structures.

    :param position_request: Complete position data including name and description
    :param current_user: Authenticated user with position creation privileges
    :param position_service: Service layer handling position creation logic
    :return: Complete details of the newly created position including generated ID
    """
    return await position_service.add_position(position_request)


@router.get(
    "",
    response_model=list[PositionResponseDTO],
    summary="Get all positions",
    responses={
        200: {
            "model": list[PositionResponseDTO],
            "description": "List of positions",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a comprehensive list of all job positions available in the organizational structure. "
    "This endpoint provides complete position data including names, identifiers, and metadata. "
    "Essential for HR operations, employee assignments, and organizational reporting. "
    "Results include both active and inactive positions for complete organizational visibility.",
)
async def get_all_positions(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.POSITION_READ]
    ),
    position_service: IPositionService = Depends(get_position_service),
) -> list[PositionResponseDTO]:
    """
    Retrieves the complete catalog of organizational positions.

    This endpoint returns all job positions defined within the organizational structure,
    providing essential data for HR management, employee assignment processes, and
    organizational planning. The response includes comprehensive position information
    necessary for maintaining accurate reporting relationships and job classifications.

    :param current_user: Authenticated user with position read privileges
    :param position_service: Service layer handling position retrieval operations
    :return: Complete list of all organizational positions with full details
    """
    return await position_service.get_all_positions()


@router.get(
    "/paginated",
    response_model=PositionPage,
    summary="Get positions with pagination",
    responses={
        200: {"model": PositionPage, "description": "Paginated list of positions"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves organizational positions using advanced pagination for optimal performance with large datasets. "
    "Supports configurable page size and navigation for efficient position browsing in HR systems. "
    "Includes total count metadata for accurate pagination controls and enhanced user experience. "
    "Ideal for position selection interfaces and large-scale organizational management tools.",
)
async def get_paginated_positions(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of positions per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.POSITION_READ]
    ),
    position_service: IPositionService = Depends(get_position_service),
) -> PositionPage:
    """
    Retrieves organizational positions with optimized pagination support.

    This endpoint provides efficient access to position data through paginated results,
    essential for managing large organizational structures. Includes comprehensive
    pagination metadata for building responsive user interfaces and maintaining
    optimal system performance during position browsing and selection operations.

    :param page: Target page number (1-based indexing)
    :param size: Maximum number of positions per page (recommended: 10-50)
    :param current_user: Authenticated user with position read access
    :param position_service: Service layer managing paginated position retrieval
    :return: Paginated position results with navigation metadata
    """
    return await position_service.get_positions_paginated(page, size)


@router.get(
    "/search",
    response_model=PositionPage,
    summary="Search positions by term",
    responses={
        200: {"model": PositionPage, "description": "Paginated list of positions"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs intelligent search across job positions using flexible text matching algorithms. "
    "Supports partial name matching, fuzzy search capabilities, and comprehensive result filtering. "
    "Returns paginated results with relevance ranking for efficient position discovery. "
    "Essential for HR operations, employee assignment workflows, and organizational analysis.",
)
async def find_positions(
    search_term: str | None = Query(
        None, description="Search term to filter positions"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of positions per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.POSITION_READ]
    ),
    position_service: IPositionService = Depends(get_position_service),
) -> PositionPage:
    """
    Performs advanced search operations across organizational positions.

    This endpoint enables sophisticated position discovery using flexible search criteria.
    Implements intelligent text matching against position names and descriptions,
    supporting both exact and partial matches for comprehensive result coverage.
    Essential for HR workflows requiring quick position identification and selection.

    :param search_term: Text query for position name matching (optional)
    :param page: Result page number for pagination navigation
    :param size: Maximum positions per page (optimized for UI performance)
    :param current_user: Authenticated user with position search privileges
    :param position_service: Service handling search logic and result processing
    :return: Paginated search results with matching positions
    """
    return await position_service.find(page, size, search_term)


@router.delete(
    "/bulk",
    response_model=MessageResponse,
    summary="Delete multiple positions by IDs",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Positions deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs bulk deletion of multiple job positions in a single optimized operation. "
    "Validates each position for dependencies and active assignments before removal. "
    "Implements transactional processing to ensure organizational integrity and provides "
    "detailed feedback on operation success. Critical operation requiring elevated permissions.",
)
async def delete_positions_bulk(
    position_ids: list[int] = Body(..., description="List of position IDs to delete"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.POSITION_DELETE]
    ),
    position_service: IPositionService = Depends(get_position_service),
) -> MessageResponse:
    """
    Executes bulk deletion of multiple organizational positions.

    This endpoint enables efficient removal of multiple positions through a single
    transactional operation. Performs comprehensive validation for each position
    to ensure no active employee assignments or organizational dependencies exist
    before proceeding with deletion. Maintains organizational integrity throughout
    the bulk operation process.

    :param position_ids: List of unique identifiers for positions to delete
    :param current_user: Authenticated user with bulk deletion privileges
    :param position_service: Service layer handling bulk deletion logic
    :return: Operation summary with deletion results and any warnings
    """
    return await position_service.delete_positions_by_ids(position_ids)


@router.post(
    "/export-excel",
    response_class=Response,
    summary="Export positions to Excel",
    responses={
        200: {"description": "Excel file containing the requested positions"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "No positions found to export"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates comprehensive Excel reports containing detailed position information for specified job roles. "
    "Creates professionally formatted spreadsheets with complete position data including names, identifiers, "
    "and organizational metadata. Ideal for HR reporting, organizational analysis, compliance documentation, "
    "and external reporting requirements. Supports bulk export with optimized file generation.",
)
async def export_positions_to_excel(
    position_ids: list[int] = Body(..., description="List of position IDs to export"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.POSITION_READ]
    ),
    position_service: IPositionService = Depends(get_position_service),
) -> Response:
    """
    Generates comprehensive Excel reports for selected organizational positions.

    This endpoint creates professionally formatted Excel spreadsheets containing
    detailed position information for reporting, analysis, and compliance purposes.
    The generated files include complete position metadata, organizational context,
    and formatting optimized for business use and external sharing.

    :param position_ids: List of unique identifiers for positions to include in export
    :param current_user: Authenticated user with position export privileges
    :param position_service: Service layer handling Excel generation logic
    :return: Excel file as downloadable response with appropriate headers
    """
    excel_data = await position_service.export_positions_to_excel(position_ids)

    current_datetime = datetime.now().strftime("%d%m%Y%H%M")
    filename = f"{current_datetime}.xlsx"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    return Response(content=excel_data, headers=headers)


@router.get(
    "/{position_id}",
    response_model=PositionResponseDTO,
    summary="Get position by ID",
    responses={
        200: {"model": PositionResponseDTO, "description": "Position found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive details for a specific job position using its unique identifier. "
    "Provides complete position information including metadata, creation timestamps, and associated data. "
    "Essential for position verification, employee assignment processes, and detailed organizational reporting. "
    "Returns full position context for administrative and HR management operations.",
)
async def get_position_by_id(
    position_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.POSITION_READ]
    ),
    position_service: IPositionService = Depends(get_position_service),
) -> PositionResponseDTO:
    """
    Retrieves detailed information for a specific organizational position.

    This endpoint provides comprehensive access to position data using the unique
    position identifier. Essential for HR operations requiring complete position
    context, including employee assignment verification, organizational reporting,
    and administrative workflows requiring position validation.

    :param position_id: Unique identifier for the target position
    :param current_user: Authenticated user with position read permissions
    :param position_service: Service layer handling position retrieval logic
    :return: Complete position details including all metadata
    """
    return await position_service.get_position_by_id(position_id)


@router.put(
    "/{position_id}",
    response_model=PositionResponseDTO,
    summary="Update existing position",
    responses={
        200: {
            "model": PositionResponseDTO,
            "description": "Position updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Position not found"},
        409: {"model": ConflictError, "description": "Position name already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates an existing job position with new information while maintaining organizational integrity. "
    "Validates name uniqueness across the organization and preserves existing employee assignments. "
    "Includes comprehensive validation to prevent conflicts and ensures consistent organizational structure. "
    "Changes are immediately reflected in all dependent systems and reporting structures.",
)
async def update_position(
    position_id: int,
    position_request: PositionRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.POSITION_UPDATE]
    ),
    position_service: IPositionService = Depends(get_position_service),
) -> PositionResponseDTO:
    """
    Updates an existing organizational position with new information.

    This endpoint enables modification of position details while maintaining organizational
    integrity and consistency. Performs comprehensive validation to ensure position names
    remain unique and that changes don't create conflicts with existing assignments or
    reporting structures. All updates are immediately reflected across dependent systems.

    :param position_id: Unique identifier of the position to update
    :param position_request: New position data including updated name and details
    :param current_user: Authenticated user with position modification privileges
    :param position_service: Service layer handling update logic and validation
    :return: Updated position information reflecting all changes
    """
    return await position_service.update_position(position_id, position_request)


@router.delete(
    "/{position_id}",
    response_model=MessageResponse,
    summary="Delete position",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Position deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Permanently removes a job position from the organizational structure. This is a critical operation "
    "that validates position dependencies before deletion to prevent organizational integrity issues. "
    "Ensures no active employee assignments exist before allowing removal. Operation is irreversible "
    "and maintains complete audit trail for compliance and organizational tracking purposes.",
)
async def delete_position(
    position_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.POSITION_DELETE]
    ),
    position_service: IPositionService = Depends(get_position_service),
) -> MessageResponse:
    """
    Permanently removes a position from the organizational structure.

    This endpoint performs secure deletion of organizational positions with comprehensive
    validation to maintain organizational integrity. Verifies that no active employee
    assignments exist before allowing removal, preventing orphaned data and maintaining
    consistent reporting structures. This is a destructive operation that cannot be undone.

    :param position_id: Unique identifier of the position to remove
    :param current_user: Authenticated user with position deletion privileges
    :param position_service: Service layer handling deletion logic and validation
    :return: Confirmation message indicating successful removal
    """
    return await position_service.delete_position(position_id)
