from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class DriverBase(BaseModel):
    lastname: str = Field(max_length=255)
    firstname: str = Field(max_length=255)
    middlename: str | None = Field(default=None, max_length=255)

    birthdate: date

    license_serial: str = Field(max_length=20)
    license_number: str = Field(max_length=20)

    license_issue_date: date
    license_exp_date: date

    licence_foreign: bool = False

    kbm: Decimal = Field(decimal_places=2, max_digits=4)


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    lastname: str | None = Field(default=None, max_length=255)
    firstname: str | None = Field(default=None, max_length=255)
    middlename: str | None = Field(default=None, max_length=255)

    birthdate: date | None = None

    license_serial: str | None = Field(default=None, max_length=20)
    license_number: str | None = Field(default=None, max_length=20)

    license_issue_date: date | None = None
    license_exp_date: date | None = None

    licence_foreign: bool | None = None

    kbm: Decimal | None = Field(default=None, decimal_places=2, max_digits=4)


class DriverRead(DriverBase):
    id: int

    model_config = ConfigDict(from_attributes=True)