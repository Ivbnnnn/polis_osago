from pydantic import BaseModel


class SearchFilter(BaseModel):
    field: str
    value: str


class SearchRequest(BaseModel):
    model_name: str
    relations: list[str] = []
    filters: list[SearchFilter] = []