from fastapi import APIRouter, Depends

from src.sensor.service import SensorRecordService
from webapp.dependency import sensor_service_dependency
from webapp.dtos import OkDTO, WaterTankSensorRecordDTO
from webapp import metrics

router = APIRouter()


@router.post("/api/records/water-tank-sensor", status_code=201)
async def record_tank_sensor(
    sensor_record: WaterTankSensorRecordDTO,
    sensor_service: SensorRecordService = Depends(sensor_service_dependency),
) -> OkDTO:
    metrics.tank_sensor_records.labels(sensor_record.tank_code).inc()
    await sensor_service.record_tank_sensor(
        tank_code=sensor_record.tank_code,
        content=sensor_record.to_content(),
    )
    return OkDTO(ok=True)
