from fastapi import APIRouter, Depends, Query, status

from app.deps import get_fake_data_service
from app.services.fakedata import FakeDataService


router = APIRouter(
    prefix="/fake-data",
    tags=["Fake Data"],
)


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_fake_data(
    count: int = Query(default=10, ge=1, le=1000),
    service: FakeDataService = Depends(get_fake_data_service),
):
    return await service.create_full_fake_data(count)


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_fake_data(
    service: FakeDataService = Depends(get_fake_data_service),
):
    await service.clear_all_data()