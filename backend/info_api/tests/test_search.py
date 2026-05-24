import pytest


@pytest.mark.asyncio
async def test_search_insurance_companies(client):
    response = await client.post(
        "/search",
        json={
            "model_name": "InsuranceCompany",
            "relations": [],
            "filters": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0