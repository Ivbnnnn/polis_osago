from decimal import Decimal
from datetime import date
import random
from faker import Faker

from app.schemas.persons import PersonCreate
from app.schemas.addresses import AddressCreate
from app.schemas.drivers import DriverCreate
from app.schemas.vehicles import VehicleCreate
from app.schemas.vehicle_sts import STSCreate
from app.schemas.insurance_companies import InsuranceCompanyCreate


fake = Faker("ru_RU")

INSURANCE_COMPANY_NAMES = [
    "АльфаСтрахование",
    "РЕСО-Гарантия",
    "Ингосстрах",
    "СОГАЗ",
    "Росгосстрах",
    "ВСК",
    "Т-Страхование",
]


VEHICLE_MODELS = [
    ("LADA", "Granta"),
    ("LADA", "Vesta"),
    ("LADA", "Niva Travel"),
    ("Kia", "Rio"),
    ("Kia", "Ceed"),
    ("Kia", "Sportage"),
    ("Hyundai", "Solaris"),
    ("Hyundai", "Creta"),
    ("Hyundai", "Tucson"),
    ("Toyota", "Camry"),
    ("Toyota", "Corolla"),
    ("Toyota", "RAV4"),
    ("Volkswagen", "Polo"),
    ("Volkswagen", "Tiguan"),
    ("Renault", "Logan"),
    ("Renault", "Duster"),
    ("Geely", "Emgrand"),
    ("Geely", "Coolray"),
    ("Haval", "Jolion"),
    ("Haval", "F7"),
    ("Skoda", "Octavia"),
    ("Skoda", "Rapid"),
    ("Nissan", "Qashqai"),
    ("Nissan", "X-Trail"),
    ("Mazda", "CX-5"),
    ("Ford", "Focus"),
    ("Chevrolet", "Niva"),
    ("Chery", "Tiggo 7 Pro"),
    ("Omoda", "C5"),
    ("Moskvich", "3"),
]

def generate_passport_issuer() -> str:
    return fake.random_element(
        elements=[
            "ГУ МВД РОССИИ ПО Г. МОСКВЕ",
            "УМВД РОССИИ ПО БРЯНСКОЙ ОБЛАСТИ",
            "ОТДЕЛОМ УФМС РОССИИ ПО БРЯНСКОЙ ОБЛАСТИ",
            "ОТДЕЛОМ МВД РОССИИ ПО СОВЕТСКОМУ РАЙОНУ Г. БРЯНСКА",
            "ОТДЕЛОМ МВД РОССИИ ПО Г. САНКТ-ПЕТЕРБУРГУ",
            "УФМС РОССИИ ПО МОСКОВСКОЙ ОБЛАСТИ",
        ]
    )


def generate_person() -> PersonCreate:
    return PersonCreate(
        lastname=fake.last_name(),
        firstname=fake.first_name(),
        middlename=fake.middle_name(),
        birthdate=fake.date_of_birth(
            minimum_age=18,
            maximum_age=80,
        ),
        passport_serial=str(fake.random_number(digits=4, fix_len=True)),
        passport_number=str(fake.random_number(digits=6, fix_len=True)),
        passport_issue_date=fake.date_between(
            start_date="-35y",
            end_date="-1y",
        ),
        passport_issuer=generate_passport_issuer(),
        passport_code=generate_passport_code(),
        passport_foreign=False,
        phone=fake.phone_number(),
        email=fake.email(),
    )


def generate_address(person_id: int) -> AddressCreate:
    region = fake.region()
    city = fake.city()
    street = fake.street_name()
    house = str(fake.building_number())

    building = fake.random_element(elements=[None, "1", "2", "А", "Б"])
    apartment = str(fake.random_int(min=1, max=300))

    full_address = build_full_address(
        region=region,
        city=city,
        street=street,
        house=house,
        building=building,
        apartment=apartment,
    )

    return AddressCreate(
        person_id=person_id,
        full_address=full_address,
        region=region,
        city=city,
        street=street,
        house=house,
        building=building,
        apartment=apartment,
    )


def generate_driver() -> DriverCreate:
    issue_date = fake.date_between(
        start_date="-20y",
        end_date="-1y",
    )

    exp_date = date(
        issue_date.year + 10,
        issue_date.month,
        issue_date.day,
    )

    return DriverCreate(
        lastname=fake.last_name(),
        firstname=fake.first_name(),
        middlename=fake.middle_name(),
        birthdate=fake.date_of_birth(
            minimum_age=18,
            maximum_age=80,
        ),
        license_serial=str(fake.random_number(digits=4, fix_len=True)),
        license_number=str(fake.random_number(digits=6, fix_len=True)),
        license_issue_date=issue_date,
        license_exp_date=exp_date,
        licence_foreign=False,
        kbm=generate_kbm(),
    )


def generate_insurance_company_by_name(name: str) -> InsuranceCompanyCreate:
    return InsuranceCompanyCreate(
        name=name,
        commission_percent=Decimal(
            str(
                fake.pydecimal(
                    left_digits=2,
                    right_digits=2,
                    positive=True,
                    min_value=5,
                    max_value=25,
                )
            )
        ),
        koef=Decimal(
            str(
                fake.pydecimal(
                    left_digits=1,
                    right_digits=2,
                    positive=True,
                    min_value=1,
                    max_value=3,
                )
            )
        ),
    )

def generate_insurance_companies() -> list[InsuranceCompanyCreate]:
    return [
        generate_insurance_company_by_name(name)
        for name in INSURANCE_COMPANY_NAMES
    ]

def generate_vehicle() -> VehicleCreate:
    brand, model = fake.random_element(elements=VEHICLE_MODELS)

    body_number = None
    chassis_number = None

    if fake.random_int(min=1, max=100) <= 10:
        body_number = generate_body_number()

    if fake.random_int(min=1, max=100) <= 5:
        chassis_number = generate_chassis_number()

    purpose = random.choices(
        population=["personal", "taxi", "commercial"],
        weights=[0.8, 0.1, 0.1],
        k=1,
    )[0]

    return VehicleCreate(
        type=1,
        brand=brand,
        model=model,
        year=fake.random_int(min=2000, max=date.today().year),
        license_plate=generate_license_plate(),
        vin=generate_vin(),
        body_number=body_number,
        chassis_number=chassis_number,
        power_hp=fake.random_int(min=70, max=250),
        purpose=purpose,
        use_trailer=False,
    )


def generate_body_number() -> str:
    return "".join(
        fake.random_element(elements=list("ABCDEFGHJKLMNPRSTUVWXYZ0123456789"))
        for _ in range(12)
    )


def generate_chassis_number() -> str:
    return "".join(
        fake.random_element(elements=list("ABCDEFGHJKLMNPRSTUVWXYZ0123456789"))
        for _ in range(14)
    )


def generate_vehicle_doc_serial_number(doc_type: int) -> tuple[str, str]:
    if doc_type == 0:
        return generate_pts_serial_number()

    if doc_type == 1:
        return generate_sts_serial_number()

    if doc_type == 2:
        return generate_epts_serial_number()

    raise ValueError(f"Unknown vehicle document type: {doc_type}")


def generate_pts_serial_number() -> tuple[str, str]:
    serial = (
        f"{fake.random_number(digits=2, fix_len=True)}"
        f"{generate_russian_doc_letters(2)}"
    )
    number = str(fake.random_number(digits=6, fix_len=True))

    return serial, number


def generate_sts_serial_number() -> tuple[str, str]:
    serial = (
        f"{fake.random_number(digits=2, fix_len=True)}"
        f"{generate_russian_doc_letters(2)}"
    )
    number = str(fake.random_number(digits=6, fix_len=True))

    return serial, number


def generate_epts_serial_number() -> tuple[str, str]:
    serial = ""
    number = str(fake.random_number(digits=15, fix_len=True))

    return serial, number


def generate_russian_doc_letters(count: int) -> str:
    letters = "АВЕКМНОРСТУХ"

    return "".join(
        fake.random_element(elements=list(letters))
        for _ in range(count)
    )

def generate_sts(vehicle_id: int) -> STSCreate:
    doc_type = fake.random_element(elements=[0, 1, 2])
    serial, number = generate_vehicle_doc_serial_number(doc_type)

    return STSCreate(
        vehicle_id=vehicle_id,
        doc_type=doc_type,
        serial=serial,
        number=number,
        issue_date=fake.date_between(
            start_date="-10y",
            end_date="today",
        ),
    )


def generate_passport_code() -> str:
    first_part = fake.random_number(digits=3, fix_len=True)
    second_part = fake.random_number(digits=3, fix_len=True)

    return f"{first_part}-{second_part}"


def generate_license_plate() -> str:
    letters = "АВЕКМНОРСТУХ"

    first_letter = fake.random_element(elements=list(letters))
    second_letter = fake.random_element(elements=list(letters))
    third_letter = fake.random_element(elements=list(letters))

    number = fake.random_number(digits=3, fix_len=True)
    region = fake.random_element(
        elements=[
            "01", "02", "03", "04", "05", "06", "07", "08", "09",
            "10", "11", "12", "13", "14", "15", "16", "17", "18",
            "19", "21", "22", "23", "24", "25", "26", "27", "28",
            "29", "30", "31", "32", "33", "34", "35", "36", "37",
            "38", "39", "40", "41", "42", "43", "44", "45", "46",
            "47", "48", "49", "50", "51", "52", "53", "54", "55",
            "56", "57", "58", "59", "60", "61", "62", "63", "64",
            "65", "66", "67", "68", "69", "70", "71", "72", "73",
            "74", "75", "76", "77", "78", "79", "80", "81", "82",
            "83", "84", "85", "86", "87", "88", "89", "90", "91",
            "92", "93", "94", "95", "96", "97", "98", "99",

            "102", "113", "116", "121", "123", "124", "125", "126",
            "134", "136", "138", "142", "150", "152", "154", "159",
            "161", "163", "164", "173", "174", "177", "178", "186",
            "190", "196", "197", "198", "199",

            "702", "716", "750", "761", "763", "774", "777", "797",
            "799",
        ]
    )

    return f"{first_letter}{number}{second_letter}{third_letter}{region}"


def generate_vin() -> str:
    allowed_chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"

    return "".join(
        fake.random_element(elements=list(allowed_chars))
        for _ in range(17)
    )


def generate_kbm() -> Decimal:
    return fake.random_element(
        elements=[
            Decimal("0.46"),
            Decimal("0.52"),
            Decimal("0.57"),
            Decimal("0.63"),
            Decimal("0.68"),
            Decimal("0.78"),
            Decimal("0.91"),
            Decimal("1.00"),
            Decimal("1.17"),
            Decimal("1.40"),
            Decimal("1.76"),
            Decimal("2.25"),
            Decimal("2.94"),
            Decimal("3.92"),
        ]
    )


def build_full_address(
    region: str,
    city: str,
    street: str,
    house: str,
    building: str | None,
    apartment: str | None,
) -> str:
    parts = [
        region,
        city,
        f"ул. {street}",
        f"д. {house}",
    ]

    if building is not None:
        parts.append(f"к. {building}")

    if apartment is not None:
        parts.append(f"кв. {apartment}")

    return ", ".join(parts)