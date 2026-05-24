from app.repositories.base import BaseRepository
from sqlalchemy import insert
from app.models.drivers import Driver
from app.schemas.drivers import DriverCreate
class DriverRepository(BaseRepository):
    async def insert(self, data:DriverCreate):
        stmt = insert(Driver).values(**data.model_dump()).returning(Driver)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()