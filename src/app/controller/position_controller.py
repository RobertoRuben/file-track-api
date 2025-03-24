from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from src.app.dto.request import PositionRequestDTO
from src.app.dto.response import PositionResponseDTO, PositionPage
from src.app.schema import MessageResponse
from src.app.service.interfaces import IPositionService
from src.app.service.dependencies import get_position_service

router = APIRouter(prefix="/position", tags=["Position"])

position_tags_metadata = {
    "name": "Position",
    "description": "Manages positions within the system. These operations allow creating, retrieving, "
    "updating, and deleting positions, as well as searching and listing them with pagination.",
}


@router.post(
    "",
    response_model=PositionResponseDTO,
    summary="Create a new position in the system",
    status_code=201,
    responses={
        201: {
            "model": PositionResponseDTO,
            "description": "Position created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        409: {
            "model": ConflictError,
            "description": "Position already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new position in the system. Provide the position details in the request body to create it successfully.",
)
async def create_position(
    position_request: PositionRequestDTO,
    position_service: IPositionService = Depends(get_position_service),
) -> PositionResponseDTO:
    """
    Endpoint to create a new position.

    This endpoint allows the creation of a new position in the system. The position data
    must be provided in the request body. If the position is created successfully, a status code 201
    with the created position's details is returned.

    :param position_request: Request body containing position data.
    :param position_service: Service to handle the position creation logic.
    :return: The created position data.
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
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a list of all positions in the system.",
)
async def get_all_positions(
    position_service: IPositionService = Depends(get_position_service),
) -> list[PositionResponseDTO]:
    """
    Endpoint to retrieve all positions.

    This endpoint returns a list of all available positions in the system. The response will include
    all positions stored in the database.

    :param position_service: Service to handle the query and retrieve all positions.
    :return: A list of positions in the system.
    """
    return await position_service.get_all_positions()


@router.get(
    "/paginated",
    response_model=PositionPage,
    summary="Get positions with pagination",
    responses={
        200: {
            "model": PositionPage,
            "description": "Paginated list of positions",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves positions in a paginated format to manage large data sets.",
)
async def get_paginated_positions(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of positions per page"),
    position_service: IPositionService = Depends(get_position_service),
) -> PositionPage:
    """
    Endpoint to retrieve positions in a paginated manner.

    This endpoint allows retrieving positions in a paginated format. The user can specify the page number
    and the number of positions per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of positions to return per page.
    :param position_service: Service to handle the query and return paginated positions.
    :return: A paginated list of positions.
    """
    return await position_service.get_positions_paginated(page, size)


@router.get(
    "/search",
    response_model=PositionPage,
    summary="Search positions based on a term",
    responses={
        200: {
            "model": PositionPage,
            "description": "Paginated list of positions",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search positions based on a keyword or phrase, with pagination for better management of search results.",
)
async def find_positions(
    search_term: str | None = Query(
        None, description="Search term to filter positions"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of positions per page"),
    position_service: IPositionService = Depends(get_position_service),
) -> PositionPage:
    """
    Endpoint to search positions using a search term.

    This endpoint allows searching for positions based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within position names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param position_service: Service to handle the search logic and return results.
    :return: A paginated list of positions that match the search term.
    """
    return await position_service.find(page, size, search_term)


@router.get(
    "/{position_id}",
    response_model=PositionResponseDTO,
    summary="Get a specific position by ID",
    responses={
        200: {
            "model": PositionResponseDTO,
            "description": "Position found",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve details of a specific position using its ID.",
)
async def get_position_by_id(
    position_id: int,
    position_service: IPositionService = Depends(get_position_service),
) -> PositionResponseDTO:
    """
    Endpoint to retrieve a position by its ID.

    This endpoint retrieves the details of a specific position identified by its ID. If the position is found,
    the position's data is returned. If not, a 404 error is returned.

    :param position_id: The ID of the position to retrieve.
    :param position_service: Service to handle the query and retrieve the position.
    :return: The position details.
    """
    return await position_service.get_position_by_id(position_id)


@router.put(
    "/{position_id}",
    response_model=PositionResponseDTO,
    summary="Update an existing position by ID",
    responses={
        200: {
            "model": PositionResponseDTO,
            "description": "Position updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing position by its ID.",
)
async def update_position(
    position_id: int,
    position_request: PositionRequestDTO,
    position_service: IPositionService = Depends(get_position_service),
) -> PositionResponseDTO:
    """
    Endpoint to update an existing position.

    This endpoint allows updating the details of an existing position identified by its ID. If the position
    is updated successfully, the updated position data is returned. If the position is not found,
    a 404 error is returned.

    :param position_id: The ID of the position to update.
    :param position_request: The new data for the position.
    :param position_service: Service to handle the update logic.
    :return: The updated position data.
    """
    return await position_service.update_position(position_id, position_request)


@router.delete(
    "/{position_id}",
    response_model=MessageResponse,
    summary="Delete a position by ID",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Position deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific position from the system using its ID.",
)
async def delete_position(
    position_id: int,
    position_service: IPositionService = Depends(get_position_service),
) -> MessageResponse:
    """
    Endpoint to delete a position.

    This endpoint allows deleting a specific position identified by its ID. If the position is deleted
    successfully, a success message is returned. If the position is not found, a 404 error is returned.

    :param position_id: The ID of the position to delete.
    :param position_service: Service to handle the delete logic.
    :return: A success message indicating that the position has been deleted.
    """
    return await position_service.delete_position(position_id)
