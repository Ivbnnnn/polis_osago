from app.repositories.base import BaseRepository
from sqlalchemy import insert
from app.models.persons import Person
from app.schemas.persons import PersonCreate
class PersonRepository(BaseRepository):
    async def insert(self, data:PersonCreate):
        stmt = insert(Person).values(**data.model_dump()).returning(Person)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()