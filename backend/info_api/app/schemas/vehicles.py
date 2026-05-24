from pydantic import BaseModel, ConfigDict, Field, model_validator


class VehicleBase(BaseModel):
    type: int

    brand: str = Field(max_length=255)
    model: str = Field(max_length=255)

    year: int = Field(ge=1900, le=2100)

    license_plate: str = Field(max_length=20)

    vin: str | None = Field(default=None, max_length=17)
    body_number: str | None = Field(default=None, max_length=255)
    chassis_number: str | None = Field(default=None, max_length=255)

    power_hp: int = Field(gt=0)

    purpose: str = Field(max_length=255)

    use_trailer: bool = False

    @model_validator(mode="after")
    def validate_vehicle_identifier(self):
        identifiers = [
            self.vin,
            self.body_number,
            self.chassis_number,
        ]

        if not any(value and value.strip() for value in identifiers):
            raise ValueError(
                "At least one of vin, body_number or chassis_number must be provided"
            )

        return self


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    type: int | None = None

    brand: str | None = Field(default=None, max_length=255)
    model: str | None = Field(default=None, max_length=255)

    year: int | None = Field(default=None, ge=1900, le=2100)

    license_plate: str | None = Field(default=None, max_length=20)

    vin: str | None = Field(default=None, max_length=17)
    body_number: str | None = Field(default=None, max_length=255)
    chassis_number: str | None = Field(default=None, max_length=255)

    power_hp: int | None = Field(default=None, gt=0)

    purpose: str | None = Field(default=None, max_length=255)

    use_trailer: bool | None = None


class VehicleRead(VehicleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)