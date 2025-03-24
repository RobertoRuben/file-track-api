from enum import Enum


class GeneroEnum(Enum):
    """
    Enumeration representing the gender options available in the system.

    This enum restricts gender values to ensure data consistency across the application.
    It is used by entities such as Remitente that require gender specification.

    Attributes:
        Masculino: Represents male gender.
        Femenino: Represents female gender.
    """

    Masculino = "Masculino"
    Femenino = "Femenino"
