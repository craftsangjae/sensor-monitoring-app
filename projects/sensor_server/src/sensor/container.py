from src.database.container import DatabaseContainer
from dependency_injector import containers, providers

from src.facility.container import FacilityContainer
from src.sensor.repository import (
    WaterTankSensorRecordHistoryRepository,
    WaterTankSensorRecordRepository,
)
from src.sensor.service import SensorRecordService


class SensorContainer(containers.DeclarativeContainer):
    """센서 정보 저장"""

    database: DatabaseContainer = providers.Container(DatabaseContainer)
    facility: FacilityContainer = providers.Container(FacilityContainer)

    repository = providers.Singleton(
        WaterTankSensorRecordRepository,
        session_factory=database.session_factory,
    )
    history_repository = providers.Singleton(
        WaterTankSensorRecordHistoryRepository,
        session_factory=database.session_factory,
    )

    service = providers.Singleton(
        SensorRecordService,
        repository=repository,
        history_repository=history_repository,
        facility_service=facility.service,
    )
