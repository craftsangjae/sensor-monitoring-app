from fastapi import APIRouter, Depends

from src.sensor.service import SensorRecordService
from webapp.dependency import sensor_service_dependency
from webapp.dtos import OkDTO, WaterTankSensorRecordDTO

router = APIRouter()


@router.post("/water-tank-sensor")
async def record_tank_sensor(
    sensor_record: WaterTankSensorRecordDTO,
    sensor_service: SensorRecordService = Depends(sensor_service_dependency),
) -> OkDTO:
    await sensor_service.record_tank_sensor(sensor_record.to_content())
    return OkDTO()
