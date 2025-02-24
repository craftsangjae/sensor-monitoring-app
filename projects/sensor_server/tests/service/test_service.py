from datetime import datetime
import pytest

from src.facility.container import FacilityContainer
from src.facility.domains import WaterTank, WaterTankBuilding, WaterTankCenter
from src.facility.repository import (
    WaterTankBuildingRepository,
    WaterTankCenterRepository,
    WaterTankRepository,
)
from src.facility.service import FacilityService
from src.sensor.container import SensorContainer
from src.sensor.domains import WaterTankSensorRecordContent
from src.sensor.repository import (
    WaterTankSensorRecordHistoryRepository,
    WaterTankSensorRecordRepository,
)
from src.sensor.service import SensorRecordService


@pytest.fixture
def given_service(
    given_sensor_container: SensorContainer,
) -> SensorRecordService:
    return given_sensor_container.service()


@pytest.fixture
def given_facility_service(
    given_facility_container: FacilityContainer,
) -> FacilityService:
    return given_facility_container.service()


@pytest.fixture
def given_repository(
    given_sensor_container: SensorContainer,
) -> WaterTankSensorRecordRepository:
    return given_sensor_container.repository()


@pytest.fixture
def given_history_repository(
    given_sensor_container: SensorContainer,
) -> WaterTankSensorRecordHistoryRepository:
    return given_sensor_container.history_repository()


@pytest.fixture
def given_water_tank_center_repository(
    given_facility_container: FacilityContainer,
    initialize_database,
):
    """테스트용 수조 건물 생성"""
    return given_facility_container.water_tank_center_repository()


@pytest.fixture
def given_water_tank_building_repository(
    given_facility_container: FacilityContainer,
):
    """테스트용 수조 건물 생성"""
    return given_facility_container.water_tank_building_repository()


@pytest.fixture
def given_water_tank_repository(
    given_facility_container: FacilityContainer,
):
    """테스트용 수조 건물 생성"""
    return given_facility_container.water_tank_repository()


@pytest.fixture
async def given_center(
    given_water_tank_center_repository: WaterTankCenterRepository,
):
    """테스트용 수조 센터 생성"""
    center = WaterTankCenter.new(center_name="test_center")
    await given_water_tank_center_repository.save(center)
    return center


@pytest.fixture
async def given_building(
    given_water_tank_building_repository: WaterTankBuildingRepository,
    given_center: WaterTankCenter,
):
    """테스트용 수조 건물 생성"""
    building = WaterTankBuilding.new(building_name="test_building", center=given_center)
    await given_water_tank_building_repository.save(building)
    return building


@pytest.fixture
async def given_tank(
    given_water_tank_repository: WaterTankRepository,
    given_building: WaterTankBuilding,
):
    """테스트용 수조 생성"""
    tank = WaterTank.new(tank_name="test_tank", building=given_building)
    await given_water_tank_repository.save(tank)
    return tank


async def test_record_tank_sensor_multiple_times(
    given_service: SensorRecordService,
    given_repository: WaterTankSensorRecordRepository,
    given_history_repository: WaterTankSensorRecordHistoryRepository,
    given_tank: WaterTank,
):
    """수조 센서 여러 번 기록"""
    for i in range(10):
        content = WaterTankSensorRecordContent(
            temperature=20 + i,
            ph=7 + i,
            dissolved_oxygen=10 + i,
            salinity=30 + i,
            recorded_at=datetime(2025, 1, 1, 12, 0, i),
        )
        await given_service.record_tank_sensor(given_tank.tank_code, content)

    record = await given_repository.get_by_id(given_tank.tank_id)
    assert record is not None
    assert record.tank_id == given_tank.tank_id
    assert record.content.temperature == 20 + 9
    assert record.content.ph == 7 + 9
    assert record.content.dissolved_oxygen == 10 + 9

    histories = await given_history_repository.find_all()
    histories.sort(key=lambda x: x.content.recorded_at)
    assert len(histories) == 10
    for i, history in enumerate(histories):
        assert history.tank_id == given_tank.tank_id
        assert history.content.temperature == 20 + i
        assert history.content.ph == 7 + i
        assert history.content.dissolved_oxygen == 10 + i
        assert history.content.salinity == 30 + i
