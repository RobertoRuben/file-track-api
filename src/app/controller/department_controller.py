from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from src.app.dto.request import DepartmentRequestDTO
from src.app.dto.response import DepartmentResponseDTO, DepartmentPage
from src.app.schema import MessageResponse
from src.app.service.interfaces import IDepartmentService
from src.app.service.dependencies import get_department_service

router = APIRouter(prefix="/department", tags=["Departments"])

department_tags_metadata = {
    "name": "Departments",
    "description": "Manages organizational departments within the system. "
    "These departments represent the structural units of the organization "
    "and are related to employees and interdepartmental connections. "
    "Allows complete CRUD operations, advanced search, and paginated listing.",
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
        409: {"model": ConflictError, "description": "Department already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new organizational department in the system. The name must be unique and contain only alphabetic characters.",
)
async def create_department(
    department_request: DepartmentRequestDTO,
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentResponseDTO:
    """
    Endpoint to create a new department.

    This endpoint allows the creation of a new department in the system. The department data
    must be provided in the request body. If the department is created successfully, a
    status code 201 is returned with the details of the created department.

    :param department_request: Request body containing the department data.
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
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete list of all departments registered in the system, including their identifiers, names, and timestamps.",
)
async def get_all_departments(
    department_service: IDepartmentService = Depends(get_department_service),
) -> list[DepartmentResponseDTO]:
    """
    Endpoint to retrieve all departments.

    This endpoint returns a list of all available departments in the system. The response will include
    all departments stored in the database.

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
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves departments in a paginated format to manage large data sets, allowing navigation through pages and control over the number of records per page.",
)
async def get_paginated_departments(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of departments per page"),
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentPage:
    """
    Endpoint to retrieve departments in a paginated manner.

    This endpoint allows retrieving departments in a paginated format. The user can specify the page number
    and the number of departments per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of departments to return per page.
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
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs department searches based on a keyword or phrase. Results are returned paginated for better management of search results.",
)
async def find_departments(
    search_term: str | None = Query(
        None, description="Search term to filter departments"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of departments per page"),
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentPage:
    """
    Endpoint to search departments using a search term.

    This endpoint allows searching for departments based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within department names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param department_service: Service to handle the search logic and return results.
    :return: A paginated list of departments that match the search term.
    """
    return await department_service.find(page, size, search_term)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponseDTO,
    summary="Get department by ID",
    responses={
        200: {"model": DepartmentResponseDTO, "description": "Department found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete details of a specific department using its unique identifier.",
)
async def get_department_by_id(
    department_id: int,
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentResponseDTO:
    """
    Endpoint to retrieve a department by its ID.

    This endpoint retrieves the details of a specific department identified by its ID. If the department is found,
    the department's data is returned. If not, a 404 error is returned.

    :param department_id: The ID of the department to retrieve.
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
        404: {"model": NotFoundError, "description": "Department not found"},
        409: {"model": ConflictError, "description": "Department name already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing department identified by its ID. Verifies that the new name is not already in use by another department.",
)
async def update_department(
    department_id: int,
    department_request: DepartmentRequestDTO,
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentResponseDTO:
    """
    Endpoint to update an existing department.

    This endpoint allows updating the details of an existing department identified by its ID. If the department
    is updated successfully, the updated department data is returned. If the department is not found,
    a 404 error is returned.

    :param department_id: The ID of the department to update.
    :param department_request: The new data for the department.
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
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific department from the system using its ID. This operation is irreversible and may affect relationships with employees and other departments.",
)
async def delete_department(
    department_id: int,
    department_service: IDepartmentService = Depends(get_department_service),
) -> MessageResponse:
    """
    Endpoint to delete a department.

    This endpoint allows deleting a specific department identified by its ID. If the department is deleted
    successfully, a success message is returned. If the department is not found, a 404 error is returned.

    :param department_id: The ID of the department to delete.
    :param department_service: Service to handle the delete logic.
    :return: A success message indicating that the department has been deleted.
    """
    return await department_service.delete_department(department_id)
