from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError
)
from src.app.dto.request import DepartmentRequestDTO
from src.app.dto.response import DepartmentResponseDTO, DepartmentPage
from src.app.schema import MessageResponse
from src.app.service.interfaces import IDepartmentService
from src.app.service.dependencies import get_department_service

router = APIRouter(
    prefix="/department",
    tags=["Department"]
)

department_tags_metadata = {
    "name": "Department",
    "description": "Manages departments within the system. These operations allow creating, retrieving, "
                   "updating, and deleting departments, as well as searching and listing them with pagination.",
}

@router.post(
    "",
    response_model=DepartmentResponseDTO,
    summary="Create a new department in the system",
    status_code=201,
    responses={
        201: {"model": DepartmentResponseDTO, "description": "Department created successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        409: {"model": ConflictError, "description": "Department already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new department in the system. Provide the department details in the request body to create it successfully.",
)
async def create_department(
    department_request: DepartmentRequestDTO,
    department_service: IDepartmentService = Depends(get_department_service),
) -> DepartmentResponseDTO:
    """
    Endpoint to create a new department.

    This endpoint allows the creation of a new department in the system. The department data
    must be provided in the request body. If the department is created successfully, a status code 201
    with the created department's details is returned.

    :param department_request: Request body containing department data.
    :param department_service: Service to handle the department creation logic.
    :return: The created department data.
    """
    return await department_service.add_department(department_request)


@router.get(
    "",
    response_model=list[DepartmentResponseDTO],
    summary="Get all departments",
    responses={
        200: {"model": list[DepartmentResponseDTO], "description": "List of departments"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a list of all departments in the system.",
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
    description="Retrieves departments in a paginated format to manage large data sets.",
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
    summary="Search departments based on a term",
    responses={
        200: {"model": DepartmentPage, "description": "Paginated list of departments"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search departments based on a keyword or phrase, with pagination for better management of search results.",
)
async def find_departments(
    search_term: str | None = Query(None, description="Search term to filter departments"),
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
    summary="Get a specific department by ID",
    responses={
        200: {"model": DepartmentResponseDTO, "description": "Department found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve details of a specific department using its ID.",
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
    summary="Update an existing department by ID",
    responses={
        200: {"model": DepartmentResponseDTO, "description": "Department updated successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing department by its ID.",
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
    summary="Delete a department by ID",
    responses={
        200: {"model": MessageResponse, "description": "Department deleted successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Department not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific department from the system using its ID.",
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
