from dataclasses import dataclass
from datetime import datetime


@dataclass
class WaterTankSensorRecordContent:
    """센서 측정 값"""

    temperature: float
    ph: float
    recorded_at: datetime


@dataclass
class WaterTankSensorRecord:
    tank_id: int  # 수조 id

    temperature: float
    ph: float
    recorded_at: datetime

    @staticmethod
    def from_content(
        tank_id: int, content: WaterTankSensorRecordContent
    ) -> "WaterTankSensorRecord":
        return WaterTankSensorRecord(
            tank_id=tank_id,
            temperature=content.temperature,
            ph=content.ph,
            recorded_at=content.recorded_at,
        )
