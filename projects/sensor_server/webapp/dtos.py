from pydantic import BaseModel
from datetime import datetime
from pydantic import Field

from src.sensor.domains import WaterTankSensorRecordContent


class WaterTankSensorRecordDTO(BaseModel):
    tank_code: str = Field(..., description="수조 코드")
    temperature: float = Field(..., description="온도")
    ph: float = Field(..., description="pH")
    dissolved_oxygen: float = Field(..., description="용존산소")
    salinity: float = Field(..., description="염분")
    recorded_at: datetime = Field(..., description="측정 시간")

    def to_content(self) -> WaterTankSensorRecordContent:
        return WaterTankSensorRecordContent(
            temperature=self.temperature,
            ph=self.ph,
            dissolved_oxygen=self.dissolved_oxygen,
            salinity=self.salinity,
            recorded_at=self.recorded_at,
        )


class OkDTO(BaseModel):
    ok: bool = True
