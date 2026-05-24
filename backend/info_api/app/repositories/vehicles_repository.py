from app.repositories.base import BaseRepository
from sqlalchemy import insert
from app.models.vehicles import Vehicle
from app.schemas.vehicles import VehicleCreate
class VehicleRepository(BaseRepository):
    async def insert(self, data:VehicleCreate):
        stmt = insert(Vehicle).values(**data.model_dump()).returning(Vehicle)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()