from src.database.container import DatabaseContainer
from src.facility.repository import (
    WaterTankBuildingRepository,
    WaterTankCenterRepository,
    WaterTankRepository,
)
from dependency_injector import containers, providers

from src.facility.service import FacilityService


class FacilityContainer(containers.DeclarativeContainer):
    """시설 정보 저장"""

    database: DatabaseContainer = providers.Container(DatabaseContainer)

    water_tank_repository = providers.Singleton(
        WaterTankRepository, session_factory=database.session_factory
    )
    water_tank_building_repository = providers.Singleton(
        WaterTankBuildingRepository, session_factory=database.session_factory
    )
    water_tank_center_repository = providers.Singleton(
        WaterTankCenterRepository, session_factory=database.session_factory
    )

    service = providers.Singleton(
        FacilityService,
        water_tank_repository=water_tank_repository,
        water_tank_building_repository=water_tank_building_repository,
        water_tank_center_repository=water_tank_center_repository,
    )
