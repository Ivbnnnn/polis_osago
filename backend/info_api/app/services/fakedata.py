from app.services.base import BaseService
from app.utils.fake_data import (
    generate_person,
    generate_address,
    generate_driver,
    generate_vehicle,
    generate_sts,
    generate_insurance_companies,
)
from sqlalchemy import text

class FakeDataService(BaseService):
    async def create_full_fake_data(self, count: int):
        result = []

        async with self.uow:
            insurance_companies = []

            for company_data in generate_insurance_companies():
                company = await self.uow.insurance_companies.insert(
                    company_data
                )
                insurance_companies.append(company)

            for _ in range(count):
                person_data = generate_person()
                person = await self.uow.persons.insert(person_data)

                address_data = generate_address(person_id=person.id)
                address = await self.uow.addresses.insert(address_data)

                driver_data = generate_driver()
                driver = await self.uow.drivers.insert(driver_data)

                vehicle_data = generate_vehicle()
                vehicle = await self.uow.vehicles.insert(vehicle_data)

                sts_data = generate_sts(vehicle_id=vehicle.id)
                sts = await self.uow.vehicles_sts.insert(sts_data)

                result.append(
                    {
                        "person": person,
                        "address": address,
                        "driver": driver,
                        "vehicle": vehicle,
                        "sts": sts,
                    }
                )

            await self.uow.commit()

        return {
            "insurance_companies": insurance_companies,
            "items": result,
        }
    async def clear_all_data(self) -> None:
        async with self.uow:
            await self.uow.session.execute(
                text(
                    """
                    TRUNCATE TABLE
                        info_api.addresses,
                        info_api.persons,
                        info_api.drivers,
                        info_api.sts,
                        info_api.vehicles,
                        info_api.insurance_companies
                    RESTART IDENTITY CASCADE
                    """
                )
            )

            await self.uow.commit()