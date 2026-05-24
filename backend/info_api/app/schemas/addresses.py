from pydantic import BaseModel


class AddressBase(BaseModel):
    full_address:str | None = None
    region: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    building: str | None = None
    apartment: str | None = None


class AddressCreate(AddressBase):
    person_id: int


class AddressUpdate(BaseModel):
    full_address:str | None = None
    region: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    building: str | None = None
    apartment: str | None = None 


class AddressRead(AddressBase):
    id: int
    full_address:str
    person_id: int

    model_config = {
        "from_attributes": True
    }