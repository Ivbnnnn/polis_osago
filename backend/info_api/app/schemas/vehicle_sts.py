from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class STSBase(BaseModel):
    vehicle_id: int

    doc_type: int

    serial: str = Field(max_length=20)
    number: str = Field(max_length=20)

    issue_date: date


class STSCreate(STSBase):
    pass


class STSUpdate(BaseModel):
    vehicle_id: int | None = None

    doc_type: int | None = None

    serial: str | None = Field(default=None, max_length=20)
    number: str | None = Field(default=None, max_length=20)

    issue_date: date | None = None


class STSRead(STSBase):
    id: int

    model_config = ConfigDict(from_attributes=True)