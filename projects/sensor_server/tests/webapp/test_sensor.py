from httpx import AsyncClient

from src.facility.domains import WaterTank
from datetime import datetime


async def test_record_tank_sensor(
    given_test_client: AsyncClient,
    given_tank: WaterTank,
):
    for i in range(10):
        response = await given_test_client.post(
            "/api/records/water-tank-sensor",
            json={
                "tank_code": given_tank.tank_code,
                "temperature": 20,
                "ph": 7,
                "recorded_at": datetime(2025, 1, 1, 0, 0, i).isoformat(),
            },
        )

        assert response.status_code == 201
