from datetime import datetime
from fastapi import APIRouter, Depends, Query, Security, Body, Response
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.dto.request import EmployeeRequestDTO
from src.app.dto.response import (
    EmployeeResponseDTO,
    EmployeePage,
    CurrentUserResponseDTO,
)
from src.app.schema import MessageResponse
from src.app.service.interfaces import IEmployeeService
from src.app.service.dependencies import get_employee_service, get_current_user
from src.app.security.auth.constants import Scopes

router = APIRouter(prefix="/employees", tags=["Employees"])

employee_tags_metadata = {
    "name": "Employees",
    "description": "Manages employee records within the system. "
    "These endpoints handle the complete lifecycle of employee data, "
    "including personal information, department assignments, and position details. "
    "Provides CRUD operations, advanced search capabilities, and pagination features.",
}


@router.post(
    "",
    response_model=EmployeeResponseDTO,
    summary="Create a new employee",
    status_code=201,
    responses={
        201: {
            "model": EmployeeResponseDTO,
            "description": "Employee created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {"model": ConflictError, "description": "Employee already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a comprehensive employee record with complete personal information, organizational assignments, "
    "and professional details. Validates DNI uniqueness and verifies department and position assignments "
    "to ensure organizational integrity. Establishes the foundational employment relationship within "
    "the company structure for HR management and operational workflows.",
)
async def create_employee(
    employee_request: EmployeeRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.EMPLOYEE_CREATE]
    ),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeeResponseDTO:
    """
    Creates a new comprehensive employee record in the organizational system.

    This endpoint establishes a complete employee profile including personal identification,
    organizational assignments, and professional details. Validates all required business rules
    including DNI uniqueness, department and position validity, and organizational constraints.
    Created employees are immediately integrated into the HR system and organizational structure.

    :param employee_request: Complete employee data including personal and organizational information
    :param current_user: Authenticated user with employee creation privileges
    :param employee_service: Service layer handling employee creation and validation logic
    :return: Complete employee record with generated ID and system timestamps
    """
    return await employee_service.add_employee(employee_request)


@router.get(
    "",
    response_model=list[EmployeeResponseDTO],
    summary="Get all employees",
    responses={
        200: {
            "model": list[EmployeeResponseDTO],
            "description": "List of employees",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete organizational directory of all employee records with comprehensive personal "
    "information, departmental assignments, and position details. Provides a complete HR overview for "
    "organizational management, reporting purposes, and strategic workforce planning initiatives.",
)
async def get_all_employees(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.EMPLOYEE_READ]
    ),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> list[EmployeeResponseDTO]:
    """
    Retrieves the complete organizational directory of all employees in the system.

    This endpoint provides comprehensive access to the entire employee database, delivering
    complete personnel records including personal information, departmental assignments,
    and position details. Essential for HR management, organizational reporting, and
    strategic workforce planning initiatives.

    :param current_user: Authenticated user with employee read privileges for audit tracking
    :param employee_service: Service layer handling comprehensive employee data retrieval
    :return: Complete list of all employee records with full organizational context
    """
    return await employee_service.get_all_employees()


@router.get(
    "/paginated",
    response_model=EmployeePage,
    summary="Get employees with pagination",
    responses={
        200: {"model": EmployeePage, "description": "Paginated list of employees"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves employee records in an optimized paginated format for efficient management of large "
    "organizational datasets. Enables systematic navigation through employee directories with configurable "
    "page sizes, supporting HR dashboards, reporting systems, and large-scale employee data management workflows.",
)
async def get_paginated_employees(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of employees per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.EMPLOYEE_READ]
    ),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeePage:
    """
    Retrieves employee records in an optimized paginated format for large organizational datasets.

    This endpoint provides efficient access to employee data through pagination, supporting
    large-scale HR management systems and organizational directories. Optimizes performance
    for applications handling extensive employee databases while maintaining complete
    data integrity and comprehensive employee information.

    :param page: Page number for systematic navigation through employee records
    :param size: Number of employees per page for optimized data loading
    :param current_user: Authenticated user with employee read privileges
    :param employee_service: Service layer handling paginated employee data retrieval
    :return: Paginated employee collection with navigation metadata and total counts
    """
    return await employee_service.get_employees_paginated(page, size)


@router.get(
    "/search",
    response_model=EmployeePage,
    summary="Search employees by term",
    responses={
        200: {"model": EmployeePage, "description": "Paginated list of employees"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs advanced employee searches across personal identification, names, and organizational data "
    "with intelligent matching algorithms. Supports HR personnel location, directory searches, and workforce "
    "analytics with paginated results for efficient large-scale employee discovery and management workflows.",
)
async def find_employees(
    search_term: str | None = Query(
        None, description="Search term to filter employees"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of employees per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.EMPLOYEE_READ]
    ),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeePage:
    """
    Performs advanced employee searches with intelligent matching across multiple data fields.

    This endpoint provides sophisticated search capabilities for employee discovery within
    the organizational database. Utilizes advanced matching algorithms to search across
    personal identification, names, and other relevant employee data fields, delivering
    paginated results for optimal performance and user experience.

    :param search_term: Intelligent search term for employee discovery across multiple fields
    :param page: Page number for systematic navigation through search results
    :param size: Number of search results per page for optimal performance
    :param current_user: Authenticated user with employee read privileges
    :param employee_service: Service layer handling advanced search logic and result compilation
    :return: Paginated search results with comprehensive employee data and match relevance
    """
    return await employee_service.find(page, size, search_term)


@router.delete(
    "/bulk",
    response_model=MessageResponse,
    summary="Delete multiple employees by IDs",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Employees deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs bulk deletion of multiple employee records in a single atomic operation for efficient "
    "organizational restructuring. Validates all employee IDs, maintains referential integrity, and provides "
    "comprehensive audit trails for mass HR operations and organizational cleanup workflows.",
)
async def delete_employees_bulk(
    employee_ids: list[int] = Body(
        ..., description="List of employee IDs for bulk deletion operation"
    ),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.EMPLOYEE_DELETE]
    ),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> MessageResponse:
    """
    Performs efficient bulk deletion of multiple employee records in a single atomic operation.

    This endpoint enables mass employee record deletion for organizational restructuring,
    departmental closures, or large-scale HR operations. Implements comprehensive
    validation, maintains system integrity, and provides detailed audit trails for
    compliance and organizational record-keeping requirements.

    :param employee_ids: List of unique employee identifiers for bulk deletion
    :param current_user: Authenticated user with bulk employee deletion privileges
    :param employee_service: Service layer handling complex bulk deletion logic
    :return: Comprehensive operation summary with success counts and audit information
    """
    return await employee_service.delete_employees_by_ids(employee_ids)


@router.post(
    "/export-excel",
    response_class=Response,
    summary="Export employees to Excel",
    responses={
        200: {"description": "Archivo Excel con los empleados solicitados"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "No se encontraron empleados para exportar",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates comprehensive Excel reports of selected employee records with complete organizational data "
    "for HR analytics, compliance reporting, and external system integration. Provides formatted spreadsheets "
    "with professional layouts, complete employee information, and optimized data structures for business analysis.",
)
async def export_employees_to_excel(
    employee_ids: list[int] = Body(
        ..., description="List of employee IDs for Excel export generation"
    ),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.EMPLOYEE_READ]
    ),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> Response:
    """
    Generates comprehensive Excel reports of selected employee records for business analysis.

    This endpoint creates professional Excel spreadsheets containing complete employee
    data including personal information, organizational assignments, and professional
    details. Optimized for HR analytics, compliance reporting, external system
    integration, and strategic workforce planning initiatives.

    :param employee_ids: List of employee identifiers for selective data export
    :param current_user: Authenticated user with employee read privileges for audit tracking
    :param employee_service: Service layer handling Excel generation and data formatting
    :return: Excel file download response with formatted employee data and professional layout
    """
    excel_data = await employee_service.export_employees_to_excel(employee_ids)

    current_datetime = datetime.now().strftime("%d%m%Y%H%M")
    filename = f"{current_datetime}.xlsx"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    return Response(content=excel_data, headers=headers)


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponseDTO,
    summary="Get employee by ID",
    responses={
        200: {"model": EmployeeResponseDTO, "description": "Employee found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive details of a specific employee using their unique organizational identifier. "
    "Provides complete personal, professional, and organizational information for HR management, employee "
    "verification, and detailed personnel record access within the company structure.",
)
async def get_employee_by_id(
    employee_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.EMPLOYEE_READ]
    ),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeeResponseDTO:
    """
    Retrieves comprehensive details of a specific employee by their unique identifier.

    This endpoint provides detailed access to individual employee records including
    complete personal information, organizational assignments, and professional details.
    Essential for HR management, employee verification processes, and detailed
    personnel record access within organizational workflows.

    :param employee_id: Unique organizational identifier for specific employee retrieval
    :param current_user: Authenticated user with employee read privileges
    :param employee_service: Service layer handling individual employee data retrieval
    :return: Complete employee record with full organizational and personal context
    """
    return await employee_service.get_employee_by_id(employee_id)


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponseDTO,
    summary="Update existing employee",
    responses={
        200: {
            "model": EmployeeResponseDTO,
            "description": "Employee updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        409: {"model": ConflictError, "description": "Employee DNI already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates comprehensive employee information including personal details, organizational assignments, "
    "and professional data. Validates business rules, maintains data integrity, and preserves employment "
    "history while enabling complete HR record management and organizational structure modifications.",
)
async def update_employee(
    employee_id: int,
    employee_request: EmployeeRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.EMPLOYEE_UPDATE]
    ),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeeResponseDTO:
    """
    Updates comprehensive employee information with complete validation and business rule enforcement.

    This endpoint enables complete modification of employee records including personal
    information, organizational assignments, and professional details. Implements
    comprehensive validation to maintain data integrity and business rule compliance
    while preserving employment history and organizational relationships.

    :param employee_id: Unique identifier for employee record modification
    :param employee_request: Complete updated employee data with validation requirements
    :param current_user: Authenticated user with employee update privileges
    :param employee_service: Service layer handling complex update logic and validation
    :return: Updated employee record with complete organizational context and change confirmation
    """
    return await employee_service.update_employee(employee_id, employee_request)


@router.delete(
    "/{employee_id}",
    response_model=MessageResponse,
    summary="Delete employee",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Employee deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Permanently removes an employee record from the organizational system with complete data cleanup. "
    "This irreversible operation eliminates all associated employee data while maintaining referential "
    "integrity and audit trails for compliance and organizational record-keeping requirements.",
)
async def delete_employee(
    employee_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.EMPLOYEE_DELETE]
    ),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> MessageResponse:
    """
    Permanently removes an employee record from the organizational system.

    This endpoint performs comprehensive employee record deletion including all
    associated data cleanup while maintaining system integrity and compliance
    requirements. Implements safety checks and audit trail preservation for
    organizational record-keeping and legal compliance.

    :param employee_id: Unique identifier for employee record deletion
    :param current_user: Authenticated user with employee deletion privileges
    :param employee_service: Service layer handling secure deletion logic and cleanup
    :return: Confirmation message with deletion success and audit information
    """
    return await employee_service.delete_employee(employee_id)
