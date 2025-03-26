from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from src.app.dto.request import EmployeeRequestDto
from src.app.dto.response import EmployeeResponseDTO, EmployeePage
from src.app.schema import MessageResponse
from src.app.service.interfaces import IEmployeeService
from src.app.service.dependencies import get_employee_service

router = APIRouter(prefix="/employee", tags=["Employee"])

employee_tags_metadata = {
    "name": "Employee",
    "description": "Manages employees within the system. These operations allow creating, retrieving, "
    "updating, and deleting employees, as well as searching and listing them with pagination.",
}


@router.post(
    "",
    response_model=EmployeeResponseDTO,
    summary="Create a new employee in the system",
    status_code=201,
    responses={
        201: {
            "model": EmployeeResponseDTO,
            "description": "Employee created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        409: {
            "model": ConflictError,
            "description": "Employee already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new employee in the system. Provide the employee details in the request body to create it successfully.",
)
async def create_employee(
    employee_request: EmployeeRequestDto,
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeeResponseDTO:
    """
    Endpoint to create a new employee.

    This endpoint allows the creation of a new employee in the system. The employee data
    must be provided in the request body. If the employee is created successfully, a status code 201
    with the created employee's details is returned.

    :param employee_request: Request body containing employee data.
    :param employee_service: Service to handle the employee creation logic.
    :return: The created employee data.
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
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a list of all employees in the system.",
)
async def get_all_employees(
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> list[EmployeeResponseDTO]:
    """
    Endpoint to retrieve all employees.

    This endpoint returns a list of all available employees in the system. The response will include
    all employees stored in the database.

    :param employee_service: Service to handle the query and retrieve all employees.
    :return: A list of employees in the system.
    """
    return await employee_service.get_all_employees()


@router.get(
    "/paginated",
    response_model=EmployeePage,
    summary="Get employees with pagination",
    responses={
        200: {
            "model": EmployeePage,
            "description": "Paginated list of employees",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves employees in a paginated format to manage large data sets.",
)
async def get_paginated_employees(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of employees per page"),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeePage:
    """
    Endpoint to retrieve employees in a paginated manner.

    This endpoint allows retrieving employees in a paginated format. The user can specify the page number
    and the number of employees per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of employees to return per page.
    :param employee_service: Service to handle the query and return paginated employees.
    :return: A paginated list of employees.
    """
    return await employee_service.get_employees_paginated(page, size)


@router.get(
    "/search",
    response_model=EmployeePage,
    summary="Search employees based on search criteria",
    responses={
        200: {
            "model": EmployeePage,
            "description": "Paginated list of employees",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search employees based on field values, with pagination for better management of search results.",
)
async def find_employees(
    search_term: str | None = Query(
        default=None, description="Search term to filter employees"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of employees per page"),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeePage:
    """
    Endpoint to search employees using various criteria.

    This endpoint allows searching for employees based on multiple search criteria. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    """

    return await employee_service.find(page, size, search_term)


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponseDTO,
    summary="Get a specific employee by ID",
    responses={
        200: {
            "model": EmployeeResponseDTO,
            "description": "Employee found",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve details of a specific employee using their ID.",
)
async def get_employee_by_id(
    employee_id: int,
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeeResponseDTO:
    """
    Endpoint to retrieve an employee by their ID.

    This endpoint retrieves the details of a specific employee identified by their ID. If the employee is found,
    the employee's data is returned. If not, a 404 error is returned.

    :param employee_id: The ID of the employee to retrieve.
    :param employee_service: Service to handle the query and retrieve the employee.
    :return: The employee details.
    """
    return await employee_service.get_employee_by_id(employee_id)


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponseDTO,
    summary="Update an existing employee by ID",
    responses={
        200: {
            "model": EmployeeResponseDTO,
            "description": "Employee updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        409: {
            "model": ConflictError,
            "description": "Employee with this DNI already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing employee by their ID.",
)
async def update_employee(
    employee_id: int,
    employee_request: EmployeeRequestDto,
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeeResponseDTO:
    """
    Endpoint to update an existing employee.

    This endpoint allows updating the details of an existing employee identified by their ID. If the employee
    is updated successfully, the updated employee data is returned. If the employee is not found,
    a 404 error is returned.

    :param employee_id: The ID of the employee to update.
    :param employee_request: The new data for the employee.
    :param employee_service: Service to handle the update logic.
    :return: The updated employee data.
    """
    return await employee_service.update_employee(employee_id, employee_request)


@router.delete(
    "/{employee_id}",
    response_model=MessageResponse,
    summary="Delete an employee by ID",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Employee deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific employee from the system using their ID.",
)
async def delete_employee(
    employee_id: int,
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> MessageResponse:
    """
    Endpoint to delete an employee.

    This endpoint allows deleting a specific employee identified by their ID. If the employee is deleted
    successfully, a success message is returned. If the employee is not found, a 404 error is returned.

    :param employee_id: The ID of the employee to delete.
    :param employee_service: Service to handle the delete logic.
    :return: A success message indicating that the employee has been deleted.
    """
    return await employee_service.delete_employee(employee_id)
