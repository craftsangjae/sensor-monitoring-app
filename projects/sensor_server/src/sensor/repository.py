from src.database.repository import BaseRepository
from src.sensor.domains import WaterTankSensorRecord
from src.sensor.entities import (
    WaterTankSensorRecordEntity,
    WaterTankSensorRecordHistoryEntity,
)


class WaterTankSensorRecordRepository(BaseRepository[int, WaterTankSensorRecord]):
    """수조 센서 측정 값 저장"""

    entity = WaterTankSensorRecordEntity


class WaterTankSensorRecordHistoryRepository(
    BaseRepository[int, WaterTankSensorRecord]
):
    """수조 센서 측정 history 저장"""

    entity = WaterTankSensorRecordHistoryEntity
