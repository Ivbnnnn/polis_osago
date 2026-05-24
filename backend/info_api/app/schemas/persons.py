from pydantic import BaseModel, EmailStr
from datetime import date


class PersonBase(BaseModel):
    lastname: str
    firstname: str
    middlename: str
    birthdate: date

    passport_serial: str
    passport_number: str
    passport_issue_date: date
    passport_issuer: str
    passport_code: str
    passport_foreign: bool = False

    phone: str
    email: EmailStr


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    lastname: str | None = None
    firstname: str | None = None
    middlename: str | None = None
    birthdate: date | None = None

    passport_serial: str | None = None
    passport_number: str | None = None
    passport_issue_date: date | None = None
    passport_issuer: str | None = None
    passport_code: str | None = None
    passport_foreign: bool | None = None

    phone: str | None = None
    email: EmailStr | None = None


class PersonRead(PersonBase):
    id: int

    model_config = {
        "from_attributes": True
    }