import httpx
from decimal import Decimal
from typing import Any
class InfoAPIClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    
    async def _request(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        response = await self.client.request(method, path, **kwargs)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print("INFO API ERROR STATUS:", response.status_code)
            print("INFO API ERROR BODY:", response.text)
            print("REQUEST JSON:", kwargs.get("json"))
            raise e

        return response.json()
    
    
    async def get_info_for_calculation(self, data: dict) -> dict:
        person_and_address = await self._request(
            "POST",
            "/search",
            json={
                "model_name":"Person",
                "relations":["addresses"],
                "filters":[
                    {
                        "field":"lastname",
                        "value":data["lastname"]
                    },
                    {
                        "field":"firstname",
                        "value":data["firstname"]
                    },
                    {
                        "field":"middlename",
                        "value":data.get("middlename")
                    }
                ]
            },
        )
        vehicle_filter = None

        for field in ("license_plate", "vin", "body_number", "chassis_number"):
            value = data.get(field)

            if value:
                vehicle_filter = {
                    "field": field,
                    "value": value,
                }
                break

        if vehicle_filter is None:
            raise ValueError(
                "Нужно передать хотя бы одно поле: license_plate, vin, body_number или chassis_number"
            )
        vehicle_and_sts = await self._request(
            "POST",
            "/search",
            json={
                "model_name":"Vehicle",
                "relations":["sts_documents"],
                "filters":[vehicle_filter]
            },
        )
        driver = await self._request(
            "POST",
            "/search",
            json={
                "model_name":"Driver",
                "relations":[],
                "filters":[
                    {
                        "field":"license_serial",
                        "value":data.get("license_serial")
                    },
                    {
                        "field":"license_number",
                        "value":data.get("license_number")
                    }
                ]
            },
        )
        companies = []

        insurance_companies = data.get("insurance_companies")

        if insurance_companies:
            for company_name in insurance_companies:
                result = await self._request(
                    "POST",
                    "/search",
                    json={
                        "model_name": "InsuranceCompany",
                        "relations": [],
                        "filters": [
                            {
                                "field": "name",
                                "value": company_name,
                            }
                        ],
                    },
                )

                companies.extend(result)
        else:
            companies = await self._request(
                "POST",
                "/search",
                json={
                    "model_name": "InsuranceCompany",
                    "relations": [],
                    "filters": [],
                },
            )
        return {
            "person_and_address":person_and_address,
            "vehicle_and_sts":vehicle_and_sts,
            "companies":companies,
            "driver":driver
        }

    async def get_company_percent(self, insurance_company_id: int) -> Decimal:
        result = await self._request(
            "POST",
            "/search",
            json={
                "model_name":"InsuranceCompany",
                "relations":[],
                "filters":[
                    {
                        "field":"id",
                        "value":str(insurance_company_id)
                    }
                ]
            },
        )
        return Decimal(str(result[0]["commission_percent"]))
    
    async def get_driver_by_id(self, id: int) -> Decimal:
        result = await self._request(
            "POST",
            "/search",
            json={
                "model_name":"Driver",
                "relations":[],
                "filters":[
                    {
                        "field":"id",
                        "value":str(id)
                    }
                ]
            },
        )
        return result
    async def get_owner_by_id(self, id: int) -> Decimal:
        result = await self._request(
            "POST",
            "/search",
            json={
                "model_name":"Person",
                "relations":[],
                "filters":[
                    {
                        "field":"id",
                        "value":str(id)
                    }
                ]
            },
        )
        return result
    async def get_company_by_id(self, id: int) -> Decimal:
        result = await self._request(
            "POST",
            "/search",
            json={
                "model_name":"InsuranceCompany",
                "relations":[],
                "filters":[
                    {
                        "field":"id",
                        "value":str(id)
                    }
                ]
            },
        )
        return result
    async def get_vehicle_by_id(self, id: int) -> Decimal:
        result = await self._request(
            "POST",
            "/search",
            json={
                "model_name":"Vehicle",
                "relations":[],
                "filters":[
                    {
                        "field":"id",
                        "value":str(id)
                    }
                ]
            },
        )
        return result
    
    async def get_all_insurance_companies(self):
        result = await self._request(
            "POST",
            "/search",
            json={
                "model_name":"InsuranceCompany",
                "relations":[],
                "filters":[]
            },
        )
        return result
    

    async def search(self, model_name:str, relations:list[str], filters):
        if isinstance(filters, dict):
            filters_payload = [
                {
                    "field": field,
                    "value": value,
                }
                for field, value in filters.items()
            ]
        else:
            filters_payload = [
                filter_item.model_dump()
                if hasattr(filter_item, "model_dump")
                else filter_item
                for filter_item in filters
            ]

        result = await self._request(
            "POST",
            "/search",
            json={
                "model_name":model_name,
                "relations":relations,
                "filters":filters_payload
            },
        )
        return result

