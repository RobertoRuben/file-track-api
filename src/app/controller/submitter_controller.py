from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from src.app.dto.request import SubmitterRequestDTO
from src.app.dto.response import SubmitterResponseDTO, SubmitterPage
from src.app.schema import MessageResponse
from src.app.service.interfaces import ISubmitterService
from src.app.service.dependencies import get_submitter_service

router = APIRouter(prefix="/submitter", tags=["Submitter"])

submitter_tags_metadata = {
    "name": "Submitter",
    "description": "Manages submitters within the system. These operations allow creating, retrieving, "
    "updating, and deleting submitters, as well as searching and listing them with pagination.",
}


@router.post(
    "",
    response_model=SubmitterResponseDTO,
    summary="Create a new submitter in the system",
    status_code=201,
    responses={
        201: {
            "model": SubmitterResponseDTO,
            "description": "Submitter created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        409: {"model": ConflictError, "description": "Submitter already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new submitter in the system. Provide the submitter details in the request body to create it successfully.",
)
async def create_submitter(
    submitter_request: SubmitterRequestDTO,
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterResponseDTO:
    """
    Endpoint to create a new submitter.

    This endpoint allows the creation of a new submitter in the system. The submitter data
    must be provided in the request body. If the submitter is created successfully, a status code 201
    with the created submitter's details is returned.

    :param submitter_request: Request body containing submitter data.
    :param submitter_service: Service to handle the submitter creation logic.
    :return: The created submitter data.
    """
    return await submitter_service.add_submitter(submitter_request)


@router.get(
    "",
    response_model=list[SubmitterResponseDTO],
    summary="Get all submitters",
    responses={
        200: {
            "model": list[SubmitterResponseDTO],
            "description": "List of submitters",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a list of all submitters in the system.",
)
async def get_all_submitters(
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> list[SubmitterResponseDTO]:
    """
    Endpoint to retrieve all submitters.

    This endpoint returns a list of all available submitters in the system. The response will include
    all submitters stored in the database.

    :param submitter_service: Service to handle the query and retrieve all submitters.
    :return: A list of submitters in the system.
    """
    return await submitter_service.get_all_submitters()


@router.get(
    "/paginated",
    response_model=SubmitterPage,
    summary="Get submitters with pagination",
    responses={
        200: {"model": SubmitterPage, "description": "Paginated list of submitters"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves submitters in a paginated format to manage large data sets.",
)
async def get_paginated_submitters(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of submitters per page"),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterPage:
    """
    Endpoint to retrieve submitters in a paginated manner.

    This endpoint allows retrieving submitters in a paginated format. The user can specify the page number
    and the number of submitters per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of submitters to return per page.
    :param submitter_service: Service to handle the query and return paginated submitters.
    :return: A paginated list of submitters.
    """
    return await submitter_service.get_submitters_paginated(page, size)


@router.get(
    "/search",
    response_model=SubmitterPage,
    summary="Search submitters based on a term",
    responses={
        200: {"model": SubmitterPage, "description": "Paginated list of submitters"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search submitters based on a keyword or phrase, with pagination for better management of search results.",
)
async def find_submitters(
    search_term: str | None = Query(
        None, description="Search term to filter submitters"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of submitters per page"),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterPage:
    """
    Endpoint to search submitters using a search term.

    This endpoint allows searching for submitters based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within submitter names, surnames or DNI.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param submitter_service: Service to handle the search logic and return results.
    :return: A paginated list of submitters that match the search term.
    """
    return await submitter_service.find(page, size, search_term)


@router.get(
    "/{submitter_id}",
    response_model=SubmitterResponseDTO,
    summary="Get a specific submitter by ID",
    responses={
        200: {"model": SubmitterResponseDTO, "description": "Submitter found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve details of a specific submitter using its ID.",
)
async def get_submitter_by_id(
    submitter_id: int,
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterResponseDTO:
    """
    Endpoint to retrieve a submitter by its ID.

    This endpoint retrieves the details of a specific submitter identified by its ID. If the submitter is found,
    the submitter's data is returned. If not, a 404 error is returned.

    :param submitter_id: The ID of the submitter to retrieve.
    :param submitter_service: Service to handle the query and retrieve the submitter.
    :return: The submitter details.
    """
    return await submitter_service.get_submitter_by_id(submitter_id)


@router.put(
    "/{submitter_id}",
    response_model=SubmitterResponseDTO,
    summary="Update an existing submitter by ID",
    responses={
        200: {
            "model": SubmitterResponseDTO,
            "description": "Submitter updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing submitter by its ID.",
)
async def update_submitter(
    submitter_id: int,
    submitter_request: SubmitterRequestDTO,
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterResponseDTO:
    """
    Endpoint to update an existing submitter.

    This endpoint allows updating the details of an existing submitter identified by its ID. If the submitter
    is updated successfully, the updated submitter data is returned. If the submitter is not found,
    a 404 error is returned.

    :param submitter_id: The ID of the submitter to update.
    :param submitter_request: The new data for the submitter.
    :param submitter_service: Service to handle the update logic.
    :return: The updated submitter data.
    """
    return await submitter_service.update_submitter(submitter_id, submitter_request)


@router.delete(
    "/{submitter_id}",
    response_model=MessageResponse,
    summary="Delete a submitter by ID",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Submitter deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific submitter from the system using its ID.",
)
async def delete_submitter(
    submitter_id: int,
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> MessageResponse:
    """
    Endpoint to delete a submitter.

    This endpoint allows deleting a specific submitter identified by its ID. If the submitter is deleted
    successfully, a success message is returned. If the submitter is not found, a 404 error is returned.

    :param submitter_id: The ID of the submitter to delete.
    :param submitter_service: Service to handle the delete logic.
    :return: A success message indicating that the submitter has been deleted.
    """
    return await submitter_service.delete_submitter(submitter_id)
