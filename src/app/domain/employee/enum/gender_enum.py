from enum import Enum


class GenderEnum(Enum):
    """
    Enumeration representing the gender options available in the system.

    This enum restricts gender values to ensure data consistency across the application.
    It is used by entities such as Remitente that require gender specification.

    Attributes:
        MALE: Represents male gender.
        FEMALE: Represents female gender.
    """

    MALE = "Male"
    FEMALE = "Female"
