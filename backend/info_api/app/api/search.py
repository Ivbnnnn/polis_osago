from fastapi import APIRouter, Depends, Query, status, HTTPException
from app.schemas.search_schema import SearchRequest
from app.deps import get_search_serive
from app.services.search_service import SearchService
from app.models import Address, Vehicle, STS, Person, InsuranceCompany, Driver

router = APIRouter(
    prefix="/search",
    tags=["Search Service"],
)

MODEL_MAP = {
    "Address": Address,
    "Vehicle": Vehicle,
    "STS": STS,
    "Person": Person,
    "InsuranceCompany": InsuranceCompany,
    "Driver": Driver,
}


RELATION_MAP = {
    "Address": {
        "person": Address.person,
    },
    "Vehicle": {
        "sts_documents": Vehicle.sts_documents,
    },
    "STS": {
        "vehicle": STS.vehicle,
    },
    "Person": {
        "addresses": Person.addresses,
    },
    "InsuranceCompany": {},
    "Driver": {},
}
def get_model_by_name(model_name: str):
    model = MODEL_MAP.get(model_name)

    if model is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown model: {model_name}",
        )

    return model


def get_relations_by_names(
    model_name: str,
    relation_names: list[str],
):
    available_relations = RELATION_MAP.get(model_name, {})
    relations = []

    for relation_name in relation_names:
        relation = available_relations.get(relation_name)

        if relation is None:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown relation '{relation_name}' for model '{model_name}'",
            )

        relations.append(relation)

    return relations

@router.post("")
async def search(
    data: SearchRequest,
    service: SearchService = Depends(get_search_serive),
):
    model = MODEL_MAP.get(data.model_name)

    if model is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown model: {data.model_name}",
        )

    relation_attrs = get_relations_by_names(
        data.model_name,
        data.relations,
    )

    return await service.query_search(
        model=model,
        relations=relation_attrs,
        filters=data.filters,
    )
