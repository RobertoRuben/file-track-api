from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from src.app.dto.request import HamletRequestDTO
from src.app.dto.response import HamletResponseDto, HamletPage
from src.app.schema import MessageResponse
from src.app.service.interfaces import IHamletService
from src.app.service.dependencies import get_hamlet_service

router = APIRouter(prefix="/hamlet", tags=["Hamlet"])

hamlet_tags_metadata = {
    "name": "Hamlet",
    "description": "Manages the hamlets in the system. These operations allow creating, retrieving, "
    "updating, and deleting hamlets, as well as searching and listing them with pagination.",
}


@router.post(
    "",
    response_model=HamletResponseDto,
    summary="Create a new hamlet in the system",
    status_code=201,
    responses={
        201: {
            "model": HamletResponseDto,
            "description": "Hamlet created successfully",
        },
        400: {
            "model": BackRequestError,
            "description": "Bad request error",
        },
        409: {
            "model": ConflictError,
            "description": "The hamlet already exists",
        },
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Creates a new hamlet in the system. Provide the details of the hamlet in the request body to successfully create it.",
)
async def create_hamlet(
    hamlet_request: HamletRequestDTO,
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletResponseDto:
    """
    Endpoint to create a new hamlet.

    This endpoint allows creating a new hamlet in the system. The hamlet's details
    must be provided in the request body. If the hamlet is created successfully, a
    201 status code with the created hamlet details is returned.

    :param hamlet_request: Request body containing the hamlet's details.
    :param hamlet_service: Service to handle the logic for creating the hamlet.
    :return: The created hamlet details.
    """
    return await hamlet_service.add_hamlet(hamlet_request)


@router.get(
    "",
    response_model=list[HamletResponseDto],
    summary="Get all hamlets",
    responses={
        200: {
            "model": list[HamletResponseDto],
            "description": "List of hamlets",
        },
        400: {
            "model": BackRequestError,
            "description": "Bad request error",
        },
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Retrieves a list of all hamlets in the system.",
)
async def get_all_hamlets(
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> list[HamletResponseDto]:
    """
    Endpoint to retrieve all hamlets.

    This endpoint returns a list of all the hamlets available in the system. The response will include
    all the hamlets stored in the database.

    :param hamlet_service: Service to handle the query and retrieve all hamlets.
    :return: A list of hamlets in the system.
    """
    return await hamlet_service.get_all_hamlets()


@router.get(
    "/paginated",
    response_model=HamletPage,
    summary="Get hamlets with pagination",
    responses={
        200: {
            "model": HamletPage,
            "description": "Paginated list of hamlets",
        },
        400: {
            "model": BackRequestError,
            "description": "Bad request error",
        },
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Retrieves hamlets in a paginated format to manage large sets of data.",
)
async def get_paginated_hamlets(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of hamlets per page"),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletPage:
    """
    Endpoint to retrieve hamlets in a paginated format.

    This endpoint allows retrieving hamlets in a paginated format. The user can specify the page number
    and the number of hamlets per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of hamlets to return per page.
    :param hamlet_service: Service to handle the query and return paginated hamlets.
    :return: A paginated list of hamlets.
    """
    return await hamlet_service.get_hamlets_paginated(page, size)


@router.get(
    "/search",
    response_model=HamletPage,
    summary="Search for hamlets based on search criteria",
    responses={
        200: {
            "model": HamletPage,
            "description": "Paginated list of hamlets",
        },
        400: {
            "model": BackRequestError,
            "description": "Bad request error",
        },
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Searches for hamlets based on search terms, with pagination for better management of results.",
)
async def find_hamlets(
    search_term: str | None = Query(
        default=None, description="Search term to filter hamlets"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of hamlets per page"),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletPage:
    """
    Endpoint to search for hamlets using search criteria.

    This endpoint allows searching for hamlets based on search terms. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: Term to search for in the names of the hamlets.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param hamlet_service: Service to handle the search and return results.
    :return: A paginated list of hamlets matching the search term.
    """
    return await hamlet_service.find(page, size, search_term)


@router.get(
    "/{hamlet_id}",
    response_model=HamletResponseDto,
    summary="Get a specific hamlet by ID",
    responses={
        200: {
            "model": HamletResponseDto,
            "description": "Hamlet found",
        },
        400: {
            "model": BackRequestError,
            "description": "Bad request error",
        },
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Retrieves the details of a specific hamlet by its ID.",
)
async def get_hamlet_by_id(
    hamlet_id: int,
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletResponseDto:
    """
    Endpoint to retrieve a hamlet by its ID.

    This endpoint retrieves the details of a specific hamlet identified by its ID. If the hamlet is found,
    the hamlet details are returned. If not, a 404 error is returned.

    :param hamlet_id: The ID of the hamlet to retrieve.
    :param hamlet_service: Service to handle the query and retrieve the hamlet.
    :return: The details of the hamlet.
    """
    return await hamlet_service.get_hamlet_by_id(hamlet_id)


@router.put(
    "/{hamlet_id}",
    response_model=HamletResponseDto,
    summary="Update an existing hamlet by ID",
    responses={
        200: {
            "model": HamletResponseDto,
            "description": "Hamlet updated successfully",
        },
        400: {
            "model": BackRequestError,
            "description": "Bad request error",
        },
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        409: {
            "model": ConflictError,
            "description": "A hamlet with this name already exists",
        },
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Updates the details of an existing hamlet by its ID.",
)
async def update_hamlet(
    hamlet_id: int,
    hamlet_request: HamletRequestDTO,
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletResponseDto:
    """
    Endpoint to update an existing hamlet.

    This endpoint allows updating the details of an existing hamlet identified by its ID. If the hamlet
    is successfully updated, the updated hamlet details are returned. If the hamlet is not found,
    a 404 error is returned.

    :param hamlet_id: The ID of the hamlet to update.
    :param hamlet_request: The new data for the hamlet.
    :param hamlet_service: Service to handle the update logic.
    :return: The updated hamlet details.
    """
    return await hamlet_service.update_hamlet(hamlet_id, hamlet_request)


@router.delete(
    "/{hamlet_id}",
    response_model=MessageResponse,
    summary="Delete a hamlet by ID",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Hamlet deleted successfully",
        },
        400: {
            "model": BackRequestError,
            "description": "Bad request error",
        },
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Deletes a specific hamlet from the system using its ID.",
)
async def delete_hamlet(
    hamlet_id: int,
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> MessageResponse:
    """
    Endpoint to delete a hamlet.

    This endpoint allows deleting a specific hamlet identified by its ID. If the hamlet is successfully deleted,
    a success message is returned. If the hamlet is not found, a 404 error is returned.

    :param hamlet_id: The ID of the hamlet to delete.
    :param hamlet_service: Service to handle the delete logic.
    :return: A success message indicating the hamlet has been deleted.
    """
    return await hamlet_service.delete_hamlet(hamlet_id)
