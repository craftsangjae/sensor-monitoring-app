from src.facility.domains import WaterTank, WaterTankBuilding
from src.facility.repository import (
    WaterTankBuildingRepository,
    WaterTankCenterRepository,
    WaterTankRepository,
)


class FacilityService:
    """시설 정보 서비스"""

    def __init__(
        self,
        water_tank_repository: WaterTankRepository,
        water_tank_building_repository: WaterTankBuildingRepository,
        water_tank_center_repository: WaterTankCenterRepository,
    ):
        self.water_tank_repository = water_tank_repository
        self.water_tank_building_repository = water_tank_building_repository
        self.water_tank_center_repository = water_tank_center_repository

    async def get_water_tank_by_code(self, tank_code: str) -> WaterTank:
        """코드로 수조 정보 조회"""
        return await self.water_tank_repository.get_by(tank_code=tank_code)

    async def get_water_tank_building_by_code(
        self, building_code: str
    ) -> WaterTankBuilding:
        """코드로 동 정보 조회"""
        return await self.water_tank_building_repository.get_by(
            building_code=building_code
        )
