from dataclasses import dataclass
from datetime import datetime


@dataclass
class WaterTankSensorRecordContent:
    """센서 측정 값"""

    temperature: float  # 온도
    ph: float  # 산성도
    dissolved_oxygen: float  # 용존산소
    salinity: float  # 염분
    recorded_at: datetime


@dataclass
class WaterTankSensorRecord:
    tank_id: int  # 수조 id

    content: WaterTankSensorRecordContent

    @staticmethod
    def from_content(
        tank_id: int, content: WaterTankSensorRecordContent
    ) -> "WaterTankSensorRecord":
        return WaterTankSensorRecord(
            tank_id=tank_id,
            content=content,
        )
