from src.facility.service import FacilityService
from src.sensor.domains import (
    WaterTankSensorRecordContent,
    WaterTankSensorRecord,
)
from src.sensor.repository import (
    WaterTankSensorRecordHistoryRepository,
    WaterTankSensorRecordRepository,
)


class SensorRecordService:
    """센서 측정 정보"""

    def __init__(
        self,
        repository: WaterTankSensorRecordRepository,
        history_repository: WaterTankSensorRecordHistoryRepository,
        facility_service: FacilityService,
    ):
        self.repository = repository
        self.history_repository = history_repository
        self.facility_service = facility_service

    async def record_tank_sensor(
        self, tank_code: str, content: WaterTankSensorRecordContent
    ) -> WaterTankSensorRecord:
        tank = await self.facility_service.get_water_tank_by_code(tank_code)

        record = WaterTankSensorRecord.from_content(
            tank_id=tank.tank_id,
            content=content,
        )

        await self.repository.save(record)
        await self.history_repository.create(record)
        return record
