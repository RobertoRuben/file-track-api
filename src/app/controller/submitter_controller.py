from fastapi import APIRouter, Depends, Query, Security
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.dto.request import SubmitterRequestDTO
from src.app.dto.response import (
    SubmitterResponseDTO,
    SubmitterPage,
    CurrentUserResponseDTO,
)
from src.app.schema import MessageResponse
from src.app.service.interfaces import ISubmitterService
from src.app.service.dependencies import get_submitter_service, get_current_user
from src.app.security.auth.constants import Scopes

router = APIRouter(prefix="/submitter", tags=["Submitters"])

submitter_tags_metadata = {
    "name": "Submitters",
    "description": "Manages submitters within the system. These operations allow creating, retrieving, "
    "updating, and deleting submitters, as well as searching and listing them with pagination.",
}


@router.post(
    "",
    response_model=SubmitterResponseDTO,
    summary="Create a new submitter",
    status_code=201,
    responses={
        201: {
            "model": SubmitterResponseDTO,
            "description": "Submitter created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {"model": ConflictError, "description": "Submitter already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new submitter in the system. The DNI must be unique.",
)
async def create_submitter(
    submitter_request: SubmitterRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_CREATE]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterResponseDTO:
    """
    Endpoint to create a new submitter.

    This endpoint allows the creation of a new submitter in the system. The submitter data
    must be provided in the request body. If the submitter is created successfully, a
    status code 201 is returned with the details of the created submitter.

    :param submitter_request: Request body containing the submitter data.
    :param current_user: The user creating the submitter, used for authorization.
    :param submitter_service: Service that handles the submitter creation logic.
    :return: The data of the created submitter.
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete list of all submitters registered in the system, including their identifiers, personal data, and timestamps.",
)
async def get_all_submitters(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_READ]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> list[SubmitterResponseDTO]:
    """
    Endpoint to retrieve all submitters.

    This endpoint returns a list of all available submitters in the system. The response will include
    all submitters stored in the database.

    :param current_user: The user requesting the submitters, used for authorization.
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves submitters in a paginated format to manage large data sets, allowing navigation through "
    "pages and control over the number of records per page.",
)
async def get_paginated_submitters(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of submitters per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_READ]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterPage:
    """
    Endpoint to retrieve submitters in a paginated manner.

    This endpoint allows retrieving submitters in a paginated format. The user can specify the page number
    and the number of submitters per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of submitters to return per page.
    :param current_user: The user requesting the submitters, used for authorization.
    :param submitter_service: Service to handle the query and return paginated submitters.
    :return: A paginated list of submitters.
    """
    return await submitter_service.get_submitters_paginated(page, size)


@router.get(
    "/search",
    response_model=SubmitterPage,
    summary="Search submitters by term",
    responses={
        200: {"model": SubmitterPage, "description": "Paginated list of submitters"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs submitter searches based on a keyword or phrase. Results are returned paginated for better "
    "management of search results.",
)
async def find_submitters(
    search_term: str | None = Query(
        None, description="Search term to filter submitters"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of submitters per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_READ]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterPage:
    """
    Endpoint to search submitters using a search term.

    This endpoint allows searching for submitters based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within submitter names, surnames or DNI.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user requesting the search, used for authorization.
    :param submitter_service: Service to handle the search logic and return results.
    :return: A paginated list of submitters that match the search term.
    """
    return await submitter_service.find(page, size, search_term)


@router.get(
    "/{submitter_id}",
    response_model=SubmitterResponseDTO,
    summary="Get submitter by ID",
    responses={
        200: {"model": SubmitterResponseDTO, "description": "Submitter found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete details of a specific submitter using its unique identifier.",
)
async def get_submitter_by_id(
    submitter_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_READ]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterResponseDTO:
    """
    Endpoint to retrieve a submitter by its ID.

    This endpoint retrieves the details of a specific submitter identified by its ID. If the submitter is found,
    the submitter's data is returned. If not, a 404 error is returned.

    :param submitter_id: The ID of the submitter to retrieve
    :param current_user: The user requesting the submitter, used for authorization.
    :param submitter_service: Service to handle the query and retrieve the submitter
    :return: The details of the submitter with the specified ID
    """
    return await submitter_service.get_submitter_by_id(submitter_id)


@router.put(
    "/{submitter_id}",
    response_model=SubmitterResponseDTO,
    summary="Update existing submitter",
    responses={
        200: {
            "model": SubmitterResponseDTO,
            "description": "Submitter updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        409: {"model": ConflictError, "description": "Submitter DNI already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing submitter identified by its ID. Verifies that the new DNI is not already in use by another submitter.",
)
async def update_submitter(
    submitter_id: int,
    submitter_request: SubmitterRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_UPDATE]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> SubmitterResponseDTO:
    """
    Endpoint to update an existing submitter.

    This endpoint allows updating the details of an existing submitter identified by its ID. If the submitter
    is updated successfully, the updated submitter data is returned. If the submitter is not found,
    a 404 error is returned.

    :param submitter_id: The ID of the submitter to update.
    :param submitter_request: The new data for the submitter.
    :param current_user: The user updating the submitter, used for authorization.
    :param submitter_service: Service to handle the update logic.
    :return: The updated submitter data.
    """
    return await submitter_service.update_submitter(submitter_id, submitter_request)


@router.delete(
    "/{submitter_id}",
    response_model=MessageResponse,
    summary="Delete submitter",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Submitter deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Submitter not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific submitter from the system using its ID. This operation is irreversible.",
)
async def delete_submitter(
    submitter_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.SUBMITTER_DELETE]
    ),
    submitter_service: ISubmitterService = Depends(get_submitter_service),
) -> MessageResponse:
    """
    Endpoint to delete a submitter.

    This endpoint allows deleting a specific submitter identified by its ID. If the submitter is deleted
    successfully, a success message is returned. If the submitter is not found, a 404 error is returned.

    :param submitter_id: The ID of the submitter to delete.
    :param current_user: The user deleting the submitter, used for authorization.
    :param submitter_service: Service to handle the delete logic.
    :return: A success message indicating that the submitter has been deleted.
    """
    return await submitter_service.delete_submitter(submitter_id)
