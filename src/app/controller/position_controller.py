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

router = APIRouter(prefix="/position", tags=["Positions"])

position_tags_metadata = {
    "name": "Positions",
    "description": "Manages positions within the system. "
    "These positions represent job roles that employees can hold. "
    "Allows complete CRUD operations, advanced search, and paginated listing.",
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
        409: {"model": ConflictError, "description": "Position already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new position in the system. The name must be unique.",
)
async def create_position(
    position_request: PositionRequestDTO,
    position_service: IPositionService = Depends(get_position_service),
) -> PositionResponseDTO:
    """
    Endpoint to create a new position.

    This endpoint allows the creation of a new position in the system. The position data
    must be provided in the request body. If the position is created successfully, a
    status code 201 is returned with the details of the created position.

    :param position_request: Request body containing the position data.
    :param position_service: Service that handles the position creation logic.
    :return: The data of the created position.
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
    description="Retrieves the complete list of all positions registered in the system, including their identifiers, names, and timestamps.",
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
        200: {"model": PositionPage, "description": "Paginated list of positions"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves positions in a paginated format to manage large data sets, allowing navigation through pages and control over the number of records per page.",
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
    summary="Search positions by term",
    responses={
        200: {"model": PositionPage, "description": "Paginated list of positions"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs position searches based on a keyword or phrase. Results are returned paginated for better management of search results.",
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
    summary="Get position by ID",
    responses={
        200: {"model": PositionResponseDTO, "description": "Position found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete details of a specific position using its unique identifier.",
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
    summary="Update existing position",
    responses={
        200: {
            "model": PositionResponseDTO,
            "description": "Position updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Position not found"},
        409: {"model": ConflictError, "description": "Position name already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing position identified by its ID. Verifies that the new name is not already in use by another position.",
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
    summary="Delete position",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Position deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Position not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific position from the system using its ID. This operation is irreversible and may affect relationships with other entities.",
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
