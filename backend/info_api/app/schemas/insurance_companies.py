from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InsuranceCompanyBase(BaseModel):
    name: str = Field(max_length=255)

    commission_percent: Decimal = Field(decimal_places=2, max_digits=5)

    koef: Decimal = Field(decimal_places=2, max_digits=5)


class InsuranceCompanyCreate(InsuranceCompanyBase):
    pass


class InsuranceCompanyUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)

    commission_percent: Decimal | None = Field(
        default=None,
        decimal_places=2,
        max_digits=5,
    )

    koef: Decimal | None = Field(
        default=None,
        decimal_places=2,
        max_digits=5,
    )


class InsuranceCompanyRead(InsuranceCompanyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)