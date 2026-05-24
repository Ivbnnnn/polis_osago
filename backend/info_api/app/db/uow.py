from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.addresses_repository import AddressesRepository
from app.repositories.persons_repository import PersonRepository
from app.repositories.vehicles_repository import VehicleRepository
from app.repositories.vehicles_sts_repository import VehicleSTSRepository
from app.repositories.drivers_repository import DriverRepository
from app.repositories.insurance_companies_repository import InsuranceCompanyRepository

class UnitOfWork():
    def __init__(self, session: AsyncSession):
        self.session = session
        self.addresses = AddressesRepository(session=session)
        self.persons = PersonRepository(session=session)
        self.vehicles = VehicleRepository(session=session)
        self.vehicles_sts = VehicleSTSRepository(session=session)
        self.drivers = DriverRepository(session=session)
        self.insurance_companies = InsuranceCompanyRepository(session=session)
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
            
    async def commit(self):
        await self.session.commit()
    async def rollback(self):
        await self.session.rollback()
