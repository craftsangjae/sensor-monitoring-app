from src.database.repository import BaseRepository
from src.facility.domains import (
    WaterTank,
    WaterTankBuilding,
    WaterTankCenter,
)
from src.facility.entities import (
    WaterTankEntity,
    WaterTankBuildingEntity,
    WaterTankCenterEntity,
)


class WaterTankRepository(BaseRepository[int, WaterTank]):
    """수조 정보 저장"""

    entity = WaterTankEntity


class WaterTankBuildingRepository(BaseRepository[int, WaterTankBuilding]):
    """동 정보 저장"""

    entity = WaterTankBuildingEntity


class WaterTankCenterRepository(BaseRepository[int, WaterTankCenter]):
    """센터 정보 저장"""

    entity = WaterTankCenterEntity
