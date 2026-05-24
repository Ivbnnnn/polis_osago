from app.repositories.base import BaseRepository
from sqlalchemy import insert
from app.models.vehicles_sts import STS
from app.schemas.vehicle_sts import STSCreate
class VehicleSTSRepository(BaseRepository):
    async def insert(self, data:STSCreate):
        stmt = insert(STS).values(**data.model_dump()).returning(STS)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()