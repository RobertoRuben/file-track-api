from src.app.schema import Page
from pydantic import BaseModel, Field
from datetime import datetime


class SettlementReponseDTO(BaseModel):
    """
    DTO for settlement response.
    Represents the data structure returned when querying settlements.
    """

    id: int = Field(..., description="ID of the settlement")
    nombre: str = Field(..., description="Name of the settlement")
    fecha_creacion: datetime = Field(..., description="Creation date of the settlement")
    fecha_modificacion: datetime = Field(
        ..., description="Modification date of the settlement"
    )


class SettlementPage(Page):
    """
    DTO for paginated response of settlements.
    Represents a paginated collection of settlement data.
    """

    data: list[SettlementReponseDTO] = Field(..., description="List of settlements")
