from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.db.uow import UnitOfWork
from app.services.fakedata import FakeDataService
from app.services.search_service import SearchService

async def get_uow(
    session: AsyncSession = Depends(get_session),
) -> UnitOfWork:
    return UnitOfWork(session)


def get_fake_data_service(
    uow: UnitOfWork = Depends(get_uow),
) -> FakeDataService:
    return FakeDataService(uow)

def get_search_serive(
    uow: UnitOfWork = Depends(get_uow),
) -> SearchService:
    return SearchService(uow)


