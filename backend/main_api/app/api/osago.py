from fastapi import APIRouter, Depends, Query, status

from app.deps import get_calculation_service, get_info_api_client, get_current_user_id
from app.services.calculation import CalculationService
from app.schemas import CalculationRequest, CalculationChooseOffer, PayOffer, SearchRequest
from app.clients.info_api import InfoAPIClient
router = APIRouter(
    prefix="/osago",
    tags=["Osago"],
)


@router.post("/search", status_code=status.HTTP_201_CREATED)
async def search(
    data:SearchRequest,
    info_api:InfoAPIClient = Depends(get_info_api_client)
):
    result =  await info_api.search(data.model_name, data.relations, data.filters)
    return result

@router.post("/get_offers", status_code=status.HTTP_201_CREATED)
async def get_offers(
    data:CalculationRequest,
    user_id: int = Depends(get_current_user_id),
    service: CalculationService = Depends(get_calculation_service),
    info_api:InfoAPIClient = Depends(get_info_api_client)
):
    result =  await service.make_offers(data, info_api, agent_id=user_id)
    return result


@router.post("/choose_offer", status_code=status.HTTP_201_CREATED)
async def choose_offer(
    data:CalculationChooseOffer,
    user_id: int = Depends(get_current_user_id),
    service: CalculationService = Depends(get_calculation_service)
):
    result =  await service.choose_offer(user_id, data.company_id, data.calculation_id)
    return result

@router.post("/pay_offer", status_code=status.HTTP_201_CREATED)
async def pay_offer(
    data:PayOffer,
    user_id: int = Depends(get_current_user_id),
    service: CalculationService = Depends(get_calculation_service),
    info_api: InfoAPIClient = Depends(get_info_api_client)
):
    result =  await service.pay_offer(user_id, data.calculation_id, info_api)
    return result


@router.post("/cancel_offer", status_code=status.HTTP_201_CREATED)
async def cancel_offer(
    data:CalculationChooseOffer,
    user_id: int = Depends(get_current_user_id),
    service: CalculationService = Depends(get_calculation_service),
):
    result =  await service.cancel_offers(user_id, data.company_id, data.calculation_id)
    return result


@router.get("/companies", status_code=status.HTTP_201_CREATED)
async def get_companies(
    service: CalculationService = Depends(get_calculation_service),
    info_api: InfoAPIClient = Depends(get_info_api_client)
):
    result =  await service.get_insurance_companies(info_api)
    return result

