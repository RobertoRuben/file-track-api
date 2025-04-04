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
        409: {"model": ConflictError, "description": "Employee already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new employee record in the system with personal information, department assignment and "
    "position details. The DNI must be unique.",
)
async def create_employee(
    employee_request: EmployeeRequestDto,
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeeResponseDTO:
    """
    Endpoint to create a new employee.

    This endpoint allows the creation of a new employee in the system. The employee data
    must be provided in the request body. If the employee is created successfully, a
    status code 201 is returned with the details of the created employee.

    :param employee_request: Request body containing the employee data
    :param employee_service: Service that handles the employee creation logic
    :return: The data of the created employee
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
    description="Retrieves the complete list of all employees registered in the system, including their personal "
    "information, department assignments and position details.",
)
async def get_all_employees(
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> list[EmployeeResponseDTO]:
    """
    Endpoint to retrieve all employees.

    This endpoint returns a list of all available employees in the system. The response will include
    all employees stored in the database.

    :param employee_service: Service to handle the query and retrieve all employees
    :return: A list of employees in the system
    """
    return await employee_service.get_all_employees()


@router.get(
    "/paginated",
    response_model=EmployeePage,
    summary="Get employees with pagination",
    responses={
        200: {"model": EmployeePage, "description": "Paginated list of employees"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves employees in a paginated format to manage large datasets, allowing navigation through pages"
    " and control over the number of records per page.",
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

    :param page: The page number to retrieve
    :param size: The number of employees to return per page
    :param employee_service: Service to handle the query and return paginated employees
    :return: A paginated list of employees
    """
    return await employee_service.get_employees_paginated(page, size)


@router.get(
    "/search",
    response_model=EmployeePage,
    summary="Search employees by term",
    responses={
        200: {"model": EmployeePage, "description": "Paginated list of employees"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs employee searches based on names, surnames, or DNI. Results are returned paginated for better"
    " management of search results.",
)
async def find_employees(
    search_term: str | None = Query(
        None, description="Search term to filter employees"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of employees per page"),
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeePage:
    """
    Endpoint to search employees using a search term.

    This endpoint allows searching for employees based on a given term. Results are returned in a
    paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: Term to search in employee names, surnames, or DNI
    :param page: The page number to retrieve
    :param size: The number of results per page
    :param employee_service: Service to handle the search logic and return the results
    :return: A paginated list of employees that match the search term
    """
    return await employee_service.find(page, size, search_term)


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponseDTO,
    summary="Get employee by ID",
    responses={
        200: {"model": EmployeeResponseDTO, "description": "Employee found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Employee not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete details of a specific employee using their unique identifier.",
)
async def get_employee_by_id(
    employee_id: int,
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeeResponseDTO:
    """
    Endpoint to retrieve an employee by their ID.

    This endpoint retrieves the details of a specific employee identified by their ID.
    If found, it returns the employee data. If not, it returns a 404 error.

    :param employee_id: ID of the employee to retrieve
    :param employee_service: Service to handle the query and retrieve the employee
    :return: Employee details
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
        404: {"model": NotFoundError, "description": "Employee not found"},
        409: {"model": ConflictError, "description": "Employee DNI already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing employee identified by their ID. Verifies that the new DNI is not "
    "already in use by another employee.",
)
async def update_employee(
    employee_id: int,
    employee_request: EmployeeRequestDto,
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> EmployeeResponseDTO:
    """
    Endpoint to update an existing employee.

    This endpoint allows updating the details of an existing employee identified by their ID.
    If the employee is updated successfully, the updated employee data is returned.
    If not found, it returns a 404 error.

    :param employee_id: ID of the employee to update
    :param employee_request: New data for the employee
    :param employee_service: Service to handle the update logic
    :return: Updated data of the employee
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
        404: {"model": NotFoundError, "description": "Employee not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific employee from the system using their ID. This operation is irreversible and removes "
    "all associated employee data.",
)
async def delete_employee(
    employee_id: int,
    employee_service: IEmployeeService = Depends(get_employee_service),
) -> MessageResponse:
    """
    Endpoint to delete an employee.

    This endpoint allows deleting a specific employee identified by their ID.
    If deleted successfully, a success message is returned.
    If not found, it returns a 404 error.

    :param employee_id: ID of the employee to delete
    :param employee_service: Service to handle the deletion logic
    :return: Success message indicating the employee has been deleted
    """
    return await employee_service.delete_employee(employee_id)
