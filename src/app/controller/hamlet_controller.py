from fastapi import APIRouter, Depends, Query, Security
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.dto.request import HamletRequestDTO
from src.app.dto.response import HamletResponseDTO, HamletPage, CurrentUserResponseDTO
from src.app.schema import MessageResponse
from src.app.service.interfaces import IHamletService
from src.app.service.dependencies import get_hamlet_service, get_current_user
from src.app.security.auth.constants import Scopes

router = APIRouter(prefix="/hamlet", tags=["Hamlets"])

hamlet_tags_metadata = {
    "name": "Hamlets",
    "description": "Manages hamlets within the system. "
    "These hamlets represent rural population units connected to settlements. "
    "Allows complete CRUD operations, advanced search, and paginated listing.",
}


@router.post(
    "",
    response_model=HamletResponseDTO,
    summary="Create a new hamlet",
    status_code=201,
    responses={
        201: {
            "model": HamletResponseDTO,
            "description": "Hamlet created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {"model": ConflictError, "description": "Hamlet already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new hamlet in the system. The name must be unique and may reference an optional settlement.",
)
async def create_hamlet(
    hamlet_request: HamletRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_CREATE]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletResponseDTO:
    """
    Endpoint to create a new hamlet.

    This endpoint allows the creation of a new hamlet in the system. The hamlet data
    must be provided in the request body. If the hamlet is created successfully, a
    status code 201 is returned with the details of the created hamlet.

    :param hamlet_request: Request body containing the hamlet data.
    :param current_user: The user creating the hamlet, used for authorization.
    :param hamlet_service: Service that handles the hamlet creation logic.
    :return: The data of the created hamlet.
    """
    return await hamlet_service.add_hamlet(hamlet_request)


@router.get(
    "",
    response_model=list[HamletResponseDTO],
    summary="Get all hamlets",
    responses={
        200: {
            "model": list[HamletResponseDTO],
            "description": "List of hamlets",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete list of all hamlets registered in the system, including their identifiers,"
    " names, and timestamps.",
)
async def get_all_hamlets(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_READ]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> list[HamletResponseDTO]:
    """
    Endpoint to retrieve all hamlets.

    This endpoint returns a list of all available hamlets in the system. The response will include
    all hamlets stored in the database.

    :param current_user: The user requesting the hamlets, used for authorization.
    :param hamlet_service: Service to handle the query and retrieve all hamlets.
    :return: A list of hamlets in the system.
    """
    return await hamlet_service.get_all_hamlets()


@router.get(
    "/paginated",
    response_model=HamletPage,
    summary="Get hamlets with pagination",
    responses={
        200: {"model": HamletPage, "description": "Paginated list of hamlets"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves hamlets in a paginated format to manage large data sets, allowing navigation through pages "
    "and control over the number of records per page.",
)
async def get_paginated_hamlets(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of hamlets per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_READ]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletPage:
    """
    Endpoint to retrieve hamlets in a paginated manner.

    This endpoint allows retrieving hamlets in a paginated format. The user can specify the page number
    and the number of hamlets per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of hamlets to return per page.
    :param current_user: The user requesting the paginated hamlets, used for authorization.
    :param hamlet_service: Service to handle the query and return paginated hamlets.
    :return: A paginated list of hamlets.
    """
    return await hamlet_service.get_hamlets_paginated(page, size)


@router.get(
    "/search",
    response_model=HamletPage,
    summary="Search hamlets by term",
    responses={
        200: {"model": HamletPage, "description": "Paginated list of hamlets"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs hamlet searches based on a keyword or phrase. Results are returned paginated for better "
    "management of search results.",
)
async def find_hamlets(
    search_term: str | None = Query(None, description="Search term to filter hamlets"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of hamlets per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_READ]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletPage:
    """
    Endpoint to search hamlets using a search term.

    This endpoint allows searching for hamlets based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within hamlet names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user performing the search, used for authorization.
    :param hamlet_service: Service to handle the search logic and return results.
    :return: A paginated list of hamlets that match the search term.
    """
    return await hamlet_service.find(page, size, search_term)


@router.get(
    "/{hamlet_id}",
    response_model=HamletResponseDTO,
    summary="Get hamlet by ID",
    responses={
        200: {"model": HamletResponseDTO, "description": "Hamlet found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete details of a specific hamlet using its unique identifier.",
)
async def get_hamlet_by_id(
    hamlet_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_READ]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletResponseDTO:
    """
    Endpoint to retrieve a hamlet by its ID.

    This endpoint retrieves the details of a specific hamlet identified by its ID. If the hamlet is found,
    the hamlet's data is returned. If not, a 404 error is returned.

    :param hamlet_id: The ID of the hamlet to retrieve.
    :param current_user: The user requesting the hamlet, used for authorization.
    :param hamlet_service: Service to handle the query and retrieve the hamlet.
    :return: The hamlet details.
    """
    return await hamlet_service.get_hamlet_by_id(hamlet_id)


@router.put(
    "/{hamlet_id}",
    response_model=HamletResponseDTO,
    summary="Update existing hamlet",
    responses={
        200: {
            "model": HamletResponseDTO,
            "description": "Hamlet updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        409: {"model": ConflictError, "description": "Hamlet name already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing hamlet identified by its ID. Verifies that the new name is not"
    " already in use by another hamlet.",
)
async def update_hamlet(
    hamlet_id: int,
    hamlet_request: HamletRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_UPDATE]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> HamletResponseDTO:
    """
    Endpoint to update an existing hamlet.

    This endpoint allows updating the details of an existing hamlet identified by its ID. If the hamlet
    is updated successfully, the updated hamlet data is returned. If the hamlet is not found,
    a 404 error is returned.

    :param hamlet_id: The ID of the hamlet to update.
    :param hamlet_request: The new data for the hamlet.
    :param current_user: The user updating the hamlet, used for authorization.
    :param hamlet_service: Service to handle the update logic.
    :return: The updated hamlet data.
    """
    return await hamlet_service.update_hamlet(hamlet_id, hamlet_request)


@router.delete(
    "/{hamlet_id}",
    response_model=MessageResponse,
    summary="Delete hamlet",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Hamlet deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Hamlet not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific hamlet from the system using its ID. This operation is irreversible and may"
    " affect relationships with other entities.",
)
async def delete_hamlet(
    hamlet_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.HAMLET_DELETE]
    ),
    hamlet_service: IHamletService = Depends(get_hamlet_service),
) -> MessageResponse:
    """
    Endpoint to delete a hamlet.

    This endpoint allows deleting a specific hamlet identified by its ID. If the hamlet is deleted
    successfully, a success message is returned. If the hamlet is not found, a 404 error is returned.

    :param hamlet_id: The ID of the hamlet to delete.
    :param current_user: The user deleting the hamlet, used for authorization.
    :param hamlet_service: Service to handle the delete logic.
    :return: A success message indicating that the hamlet has been deleted.
    """
    return await hamlet_service.delete_hamlet(hamlet_id)
