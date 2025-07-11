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
from src.app.core.schema import MessageResponse
from src.app.core.security.auth.constants import Scopes
from src.app.core.security.auth.model import CurrentUser
from src.app.core.security.auth.dependencies import get_current_user
from src.app.domain.department.dto.request import DepartmentRequestDTO
from src.app.domain.department.dto.response import DepartmentResponseDTO, DepartmentPage
from src.app.domain.department.service.interface import IDepartmentService
from src.app.domain.department.service.dependencies import get_department_service

router = APIRouter(prefix="/departments", tags=["Departments"])

department_tags_metadata = {
    "name": "Departments",
    "description": "Comprehensive enterprise organizational structure management system facilitating departmental "
    "hierarchy administration, employee assignment coordination, and interdepartmental relationship governance "
    "for effective organizational operations. Manages complex organizational units supporting HR workflows, "
    "administrative coordination, and business process optimization through structured departmental frameworks. "
    "Enables sophisticated organizational management with advanced search capabilities, bulk operations, and "
    "detailed audit trails supporting enterprise organizational governance, workforce management, and "
    "administrative efficiency across complex organizational environments.",
}


@router.post(
    "",
    response_model=DepartmentResponseDTO,
    summary="Create a new department",
    status_code=201,
    responses={
        201: {
            "model": DepartmentResponseDTO,
            "description": "Department created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {"model": ConflictError, "description": "Department already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new organizational department in the system to establish structural units within "
    "the organizational hierarchy. The department name must be unique across the entire system and follows "
    "strict validation rules including alphabetic character constraints. This endpoint establishes fundamental "
    "organizational structures that serve as the foundation for employee assignments, interdepartmental "
    "relationships, and administrative workflows. The created department becomes immediately available for "
    "employee associations and organizational management operations throughout the system.",
)
@controller_handle_exceptions
async def create_department(
    request: Request,
    department_request: DepartmentRequestDTO,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CREATE]
    ),
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentResponseDTO:
    """
    Endpoint to create a new department.

    This endpoint allows the creation of a new department in the system. The department data
    must be provided in the request body. If the department is created successfully, a
    status code 201 is returned with the details of the created department.

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param department_request: Request body containing the department data.
    :param current_user: The current user making the request, used for authorization.
    :param department_service: Service that handles the department creation logic.
    :return: The data of the created department.
    """
    return await department_service.add_department(department_request)


@router.get(
    "",
    response_model=list[DepartmentResponseDTO],
    summary="Get all departments",
    responses={
        200: {
            "model": list[DepartmentResponseDTO],
            "description": "List of departments",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete organizational structure by returning all departments registered in the system. "
    "This endpoint provides comprehensive department information including unique identifiers, names, descriptions, "
    "creation timestamps, modification dates, and associated metadata. The response delivers the full organizational "
    "hierarchy essential for administrative interface, employee assignment systems, and organizational charts. "
    "This data supports various business processes including HR management, workflow routing, and departmental "
    "reporting requirements throughout the organization.",
)
@controller_handle_exceptions
async def get_all_departments(
    request: Request,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_READ]
    ),
    department_service: IDepartmentService = Depends(get_department_service),
) -> list[DepartmentResponseDTO]:
    """
    Endpoint to retrieve all departments.

    This endpoint returns a list of all available departments in the system. The response will include
    all departments stored in the database.

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param current_user: The current user making the request, used for authorization.
    :param department_service: Service to handle the query and retrieve all departments.
    :return: A list of departments in the system.
    """
    return await department_service.get_all_departments()


@router.get(
    "/paginated",
    response_model=DepartmentPage,
    summary="Get departments with pagination",
    responses={
        200: {"model": DepartmentPage, "description": "Paginated list of departments"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Provides departments through an advanced pagination system optimized for handling large organizational "
    "structures with superior performance characteristics. This endpoint returns structured pagination metadata "
    "including total department counts, total pages, current page indicators, and navigation flags (hasNext, "
    "hasPrevious) to support sophisticated administrative interface. The pagination approach significantly "
    "enhances application responsiveness when managing extensive organizational hierarchies and enables smooth "
    "navigation through large departmental datasets in management dashboards and organizational tools.",
)
@controller_handle_exceptions
async def get_paginated_departments(
    request: Request,
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of departments per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_READ]
    ),
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentPage:
    """
    Endpoint to retrieve departments in a paginated manner.

    This endpoint allows retrieving departments in a paginated format. The user can specify the page number
    and the number of departments per page to optimize the query and reduce data overload.

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param page: The page number to retrieve.
    :param size: The number of departments to return per page.
    :param current_user: The current user making the request, used for authorization.
    :param department_service: Service to handle the query and return paginated departments.
    :return: A paginated list of departments.
    """
    return await department_service.get_departments_paginated(page, size)


@router.get(
    "/search",
    response_model=DepartmentPage,
    summary="Search departments by term",
    responses={
        200: {"model": DepartmentPage, "description": "Paginated list of departments"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Implements intelligent search capabilities across the organizational structure using sophisticated "
    "text matching algorithms to locate departments efficiently. This endpoint performs case-insensitive partial "
    "matching against department names and descriptions, enabling users to quickly discover specific departments "
    "or groups of related organizational units. The search functionality supports dynamic filtering and real-time "
    "suggestions, making it ideal for implementing auto-complete features, advanced organizational filtering systems, "
    "and department discovery tools. Results are delivered in paginated format with configurable page sizes to "
    "maintain optimal performance regardless of organizational complexity.",
)
@controller_handle_exceptions
async def find_departments(
    request: Request,
    search_term: str | None = Query(
        None, description="Search term to filter departments"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of departments per page"),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_READ]
    ),
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentPage:
    """
    Endpoint to search departments using a search term.

    This endpoint allows searching for departments based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param search_term: A term to search within department names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The current user making the request, used for authorization.
    :param department_service: Service to handle the search logic and return results.
    :return: A paginated list of departments that match the search term.
    """
    return await department_service.find(page, size, search_term)


@router.delete(
    "/bulk",
    response_model=MessageResponse,
    summary="Delete multiple departments",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Departments deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "One or more departments not found",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes bulk deletion of multiple departments in a single atomic transaction to maintain "
    "organizational integrity and system consistency. This endpoint accepts a collection of department identifiers "
    "and removes all corresponding departments from the organizational structure simultaneously. The operation "
    "follows an all-or-nothing approach - if any department cannot be deleted due to employee associations, "
    "interdepartmental dependencies, or constraints, the entire operation is rolled back to prevent partial "
    "deletions. Before execution, the system validates department existence, checks for employee assignments, "
    "verifies interdepartmental relationships, and confirms user permissions. This operation permanently affects "
    "the organizational structure and may impact employee assignments and departmental workflows throughout the system.",
)
@controller_handle_exceptions
async def delete_departments_bulk(
    request: Request,
    department_ids: list[int] = Body(
        ..., description="List of department IDs to delete"
    ),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_DELETE]
    ),
    department_service: IDepartmentService = Depends(get_department_service),
) -> MessageResponse:
    """
    Endpoint to delete multiple departments by their IDs.

    This endpoint allows deleting multiple departments in a single operation by providing their IDs.

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param department_ids: List of IDs of departments to delete
    :param current_user: The user performing the operation, used for authorization
    :param department_service: Service to handle the deletion logic
    :return: A success message indicating the result of the deletion operation
    """
    return await department_service.delete_departments_by_ids(department_ids)


@router.post(
    "/export-excel",
    response_class=Response,
    summary="Export departments to Excel",
    responses={
        200: {"description": "Excel file containing the requested departments"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "No departments found to export"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates professionally formatted Excel spreadsheets containing comprehensive organizational department data "
    "for reporting, analysis, and administrative purposes. This endpoint creates optimized Excel files with properly "
    "structured columns, formatted headers, and enhanced styling for improved readability and professional presentation. "
    "Users can specify particular departments for targeted organizational reports or export the complete departmental "
    "structure. The generated files include detailed department information such as names, descriptions, employee counts, "
    "hierarchical relationships, creation dates, and modification timestamps. Files are automatically named with timestamps "
    "to ensure uniqueness and provide audit trails. This functionality supports organizational reporting requirements, "
    "compliance documentation, and stakeholder communication needs.",
)
@controller_handle_exceptions
async def export_departments_to_excel(
    request: Request,
    department_ids: list[int] = Body(
        ..., description="List of department IDs to export"
    ),
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_READ]
    ),
    department_service: IDepartmentService = Depends(get_department_service),
) -> Response:
    """
    Endpoint to export selected departments to Excel.

    This endpoint exports the selected departments to an Excel file format.

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param department_ids: List of IDs of departments to export
    :param current_user: The user performing the export, used for authorization
    :param department_service: Service to handle the export logic
    :return: Excel file as a downloadable response
    """
    excel_data = await department_service.export_departments_to_excel(department_ids)

    current_datetime = datetime.now().strftime("%d%m%Y%H%M")
    filename = f"{current_datetime}.xlsx"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    return Response(content=excel_data, headers=headers)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponseDTO,
    summary="Get department by ID",
    responses={
        200: {"model": DepartmentResponseDTO, "description": "Department found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive details of a specific department using its unique system identifier. "
    "This endpoint returns complete department information including the department name, detailed description, "
    "organizational hierarchy position, creation timestamp, last modification date, employee counts, and "
    "associated metadata. The department ID must correspond to an existing organizational unit in the system. "
    "This endpoint is essential for displaying detailed department information in administrative interface, "
    "populating department edit forms, supporting organizational reporting, and providing context for employee "
    "management and interdepartmental operations.",
)
@controller_handle_exceptions
async def get_department_by_id(
    request: Request,
    department_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_READ]
    ),
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentResponseDTO:
    """
    Endpoint to retrieve a department by its ID.

    This endpoint retrieves the details of a specific department identified by its ID. If the department is found,
    the department's data is returned. If not, a 404 error is returned.

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param department_id: The ID of the department to retrieve.
    :param current_user: The current user making the request, used for authorization.
    :param department_service: Service to handle the query and retrieve the department.
    :return: The department details.
    """
    return await department_service.get_department_by_id(department_id)


@router.put(
    "/{department_id}",
    response_model=DepartmentResponseDTO,
    summary="Update existing department",
    responses={
        200: {
            "model": DepartmentResponseDTO,
            "description": "Department updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Department not found"},
        409: {"model": ConflictError, "description": "Department name already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the properties and organizational attributes of an existing department while maintaining "
    "system integrity and organizational consistency. This endpoint allows modification of department attributes "
    "such as name and description, with comprehensive validation to ensure the updated name remains unique across "
    "the entire organizational structure (excluding the current department being modified). The system performs "
    "thorough validation of input data, checks for naming conflicts, and automatically updates modification "
    "timestamps. Changes are immediately reflected throughout the system, affecting employee associations, "
    "organizational charts, and departmental reporting structures.",
)
@controller_handle_exceptions
async def update_department(
    request: Request,
    department_id: int,
    department_request: DepartmentRequestDTO,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_UPDATE]
    ),
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentResponseDTO:
    """
    Endpoint to update an existing department.

    This endpoint allows updating the details of an existing department identified by its ID. If the department
    is updated successfully, the updated department data is returned. If the department is not found,
    a 404 error is returned.

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param department_id: The ID of the department to update.
    :param department_request: The new data for the department.
    :param current_user: The current user making the request, used for authorization.
    :param department_service: Service to handle the update logic.
    :return: The updated department data.
    """
    return await department_service.update_department(department_id, department_request)


@router.delete(
    "/{department_id}",
    response_model=MessageResponse,
    summary="Delete department",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Department deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Permanently removes a specific department from the organizational structure using its unique identifier, "
    "with comprehensive impact assessment and dependency validation. This irreversible operation completely eliminates "
    "the department and all its associated metadata from the system. Prior to deletion, the system performs thorough "
    "checks for existing employee associations, interdepartmental relationships, and organizational dependencies to "
    "prevent data integrity violations. Employees currently assigned to this department may be affected by this "
    "operation, potentially requiring reassignment to other departments. This endpoint requires elevated administrative "
    "privileges and should be used with extreme caution in production environments.",
)
@controller_handle_exceptions
async def delete_department(
    request: Request,
    department_id: int,
    current_user: CurrentUser = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_DELETE]
    ),
    department_service: IDepartmentService = Depends(get_department_service),
) -> MessageResponse:
    """
    Endpoint to delete a department.

    This endpoint allows deleting a specific department identified by its ID. If the department is deleted
    successfully, a success message is returned. If the department is not found, a 404 error is returned.

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param department_id: The ID of the department to delete.
    :param current_user: The current user making the request, used for authorization.
    :param department_service: Service to handle the delete logic.
    :return: A success message indicating that the department has been deleted.
    """
    return await department_service.delete_department(department_id)
