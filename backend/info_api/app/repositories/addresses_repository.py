from app.repositories.base import BaseRepository
from sqlalchemy import insert, select
from app.models.addresses import Address
from app.schemas.addresses import AddressCreate
class AddressesRepository(BaseRepository):
    async def insert(self, data:AddressCreate):
        stmt = insert(Address).values(**data.model_dump()).returning(Address)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    async def get_by_person_id(self, person_id:int):
        result = (await self.session.execute(
            select(Address).where(Address.person_id == person_id)
        )).scalar_one_or_none()
        return result