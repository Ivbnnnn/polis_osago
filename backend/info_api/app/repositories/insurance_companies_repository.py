from app.repositories.base import BaseRepository
from sqlalchemy import insert
from app.models.insurance_companies import InsuranceCompany
from app.schemas.insurance_companies import InsuranceCompanyCreate
class InsuranceCompanyRepository(BaseRepository):
    async def insert(self, data:InsuranceCompanyCreate):
        stmt = insert(InsuranceCompany).values(**data.model_dump()).returning(InsuranceCompany)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()