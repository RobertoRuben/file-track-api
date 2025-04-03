from sqlmodel import (
    SQLModel,
    text,
    BIGINT,
    Field,
    CheckConstraint,
    Column,
    TEXT,
    DateTime,
)
from datetime import datetime


class Submitter(SQLModel, table=True):
    """
    Represents a person who submits documents or requests.

    Attributes:
        id: The unique identifier for the submitter
        dni: The national identification number of the submitter
        paternal_surname: The paternal last name of the submitter
        maternal_surname: The maternal last name of the submitter
        names: The name(s) of the submitter
        gender: The gender of the submitter ('Male' or 'Female')
        created_at: The timestamp when the submitter record was created
        updated_at: The timestamp when the submitter record was last updated
    """

    __tablename__ = "submitters"
    __table_args__ = (
        CheckConstraint(
            "LENGTH(paternal_surname) > 3", name="ck_submitter_paternal_surname"
        ),
        CheckConstraint(
            "LENGTH(maternal_surname) > 3", name="ck_submitter_maternal_surname"
        ),
        CheckConstraint("LENGTH(names) > 3", name="ck_submitter_names"),
        CheckConstraint(
            "dni >= 10000000 AND dni <= 99999999", name="ck_submitter_dni_range"
        ),
        CheckConstraint(
            "gender IN ('Male', 'Female')", name="ck_submitter_gender_values"
        ),
    )

    id: int | None = Field(None, sa_column=Column(BIGINT, primary_key=True))
    dni: int = Field(sa_column=Column(BIGINT, nullable=False, unique=True))
    paternal_surname: str = Field(sa_column=Column(TEXT, nullable=False))
    maternal_surname: str = Field(sa_column=Column(TEXT, nullable=False))
    names: str = Field(sa_column=Column(TEXT, nullable=False))
    gender: str = Field(sa_column=Column(TEXT, nullable=False))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
