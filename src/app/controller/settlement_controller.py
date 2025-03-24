from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from src.app.dto.request import SettlementRequestDTO
from src.app.dto.response import SettlementReponseDTO, SettlementPage
from src.app.schema import MessageResponse
from src.app.service.interfaces import ISettlementService
from src.app.service.dependencies import get_settlement_service

router = APIRouter(prefix="/settlement", tags=["Settlement"])

settlement_tags_metadata = {
    "name": "Settlement",
    "description": "Manages settlements within the system. These operations allow creating, retrieving, "
    "updating, and deleting settlements, as well as searching and listing them with pagination.",
}


@router.post(
    "",
    response_model=SettlementReponseDTO,
    summary="Create a new settlement in the system",
    status_code=201,
    responses={
        201: {
            "model": SettlementReponseDTO,
            "description": "Settlement created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        409: {"model": ConflictError, "description": "Settlement already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new settlement in the system. Provide the settlement details in the request body to create it successfully.",
)
async def create_settlement(
    settlement_request: SettlementRequestDTO,
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementReponseDTO:
    """
    Endpoint to create a new settlement.

    This endpoint allows the creation of a new settlement in the system. The settlement data
    must be provided in the request body. If the settlement is created successfully, a status code 201
    with the created settlement's details is returned.

    :param settlement_request: Request body containing settlement data.
    :param settlement_service: Service to handle the settlement creation logic.
    :return: The created settlement data.
    """
    return await settlement_service.add_settlement(settlement_request)


@router.get(
    "",
    response_model=list[SettlementReponseDTO],
    summary="Get all settlements",
    responses={
        200: {
            "model": list[SettlementReponseDTO],
            "description": "List of settlements",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a list of all settlements in the system.",
)
async def get_all_settlements(
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> list[SettlementReponseDTO]:
    """
    Endpoint to retrieve all settlements.

    This endpoint returns a list of all available settlements in the system. The response will include
    all settlements stored in the database.

    :param settlement_service: Service to handle the query and retrieve all settlements.
    :return: A list of settlements in the system.
    """
    return await settlement_service.get_all_settlements()


@router.get(
    "/paginated",
    response_model=SettlementPage,
    summary="Get settlements with pagination",
    responses={
        200: {"model": SettlementPage, "description": "Paginated list of settlements"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves settlements in a paginated format to manage large data sets.",
)
async def get_paginated_settlements(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of settlements per page"),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementPage:
    """
    Endpoint to retrieve settlements in a paginated manner.

    This endpoint allows retrieving settlements in a paginated format. The user can specify the page number
    and the number of settlements per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of settlements to return per page.
    :param settlement_service: Service to handle the query and return paginated settlements.
    :return: A paginated list of settlements.
    """
    return await settlement_service.get_settlements_paginated(page, size)


@router.get(
    "/search",
    response_model=SettlementPage,
    summary="Search settlements based on a term",
    responses={
        200: {"model": SettlementPage, "description": "Paginated list of settlements"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Settlement not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search settlements based on a keyword or phrase, with pagination for better management of search results.",
)
async def find_settlements(
    search_term: str | None = Query(
        None, description="Search term to filter settlements"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of settlements per page"),
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementPage:
    """
    Endpoint to search settlements using a search term.

    This endpoint allows searching for settlements based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within settlement names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param settlement_service: Service to handle the search logic and return results.
    :return: A paginated list of settlements that match the search term.
    """
    return await settlement_service.find(page, size, search_term)


@router.get(
    "/{settlement_id}",
    response_model=SettlementReponseDTO,
    summary="Get a specific settlement by ID",
    responses={
        200: {"model": SettlementReponseDTO, "description": "Settlement found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Settlement not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve details of a specific settlement using its ID.",
)
async def get_settlement_by_id(
    settlement_id: int,
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementReponseDTO:
    """
    Endpoint to retrieve a settlement by its ID.

    This endpoint retrieves the details of a specific settlement identified by its ID. If the settlement is found,
    the settlement's data is returned. If not, a 404 error is returned.

    :param settlement_id: The ID of the settlement to retrieve.
    :param settlement_service: Service to handle the query and retrieve the settlement.
    :return: The settlement details.
    """
    return await settlement_service.get_settlement_by_id(settlement_id)


@router.put(
    "/{settlement_id}",
    response_model=SettlementReponseDTO,
    summary="Update an existing settlement by ID",
    responses={
        200: {
            "model": SettlementReponseDTO,
            "description": "Settlement updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Settlement not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing settlement by its ID.",
)
async def update_settlement(
    settlement_id: int,
    settlement_request: SettlementRequestDTO,
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> SettlementReponseDTO:
    """
    Endpoint to update an existing settlement.

    This endpoint allows updating the details of an existing settlement identified by its ID. If the settlement
    is updated successfully, the updated settlement data is returned. If the settlement is not found,
    a 404 error is returned.

    :param settlement_id: The ID of the settlement to update.
    :param settlement_request: The new data for the settlement.
    :param settlement_service: Service to handle the update logic.
    :return: The updated settlement data.
    """
    return await settlement_service.update_settlement(settlement_id, settlement_request)


@router.delete(
    "/{settlement_id}",
    response_model=MessageResponse,
    summary="Delete a settlement by ID",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Settlement deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Settlement not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific settlement from the system using its ID.",
)
async def delete_settlement(
    settlement_id: int,
    settlement_service: ISettlementService = Depends(get_settlement_service),
) -> MessageResponse:
    """
    Endpoint to delete a settlement.

    This endpoint allows deleting a specific settlement identified by its ID. If the settlement is deleted
    successfully, a success message is returned. If the settlement is not found, a 404 error is returned.

    :param settlement_id: The ID of the settlement to delete.
    :param settlement_service: Service to handle the delete logic.
    :return: A success message indicating that the settlement has been deleted.
    """
    return await settlement_service.delete_settlement(settlement_id)
