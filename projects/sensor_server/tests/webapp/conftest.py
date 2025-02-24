from fastapi import FastAPI
import pytest

from src.facility.container import FacilityContainer
from src.facility.domains import WaterTank, WaterTankBuilding, WaterTankCenter
from src.facility.repository import (
    WaterTankBuildingRepository,
    WaterTankCenterRepository,
    WaterTankRepository,
)
from src.sensor.container import SensorContainer
from src.sensor.repository import (
    WaterTankSensorRecordHistoryRepository,
    WaterTankSensorRecordRepository,
)
from src.sensor.service import SensorRecordService
from webapp.container import ApplicationContainer
from webapp.app import create_app
from src.database.container import DatabaseContainer
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@pytest.fixture(scope="session")
def given_application_container(
    given_database_container: DatabaseContainer,
):
    return ApplicationContainer(
        database=given_database_container,
    )


@pytest.fixture(scope="session")
def given_fastapi_app(
    given_application_container: ApplicationContainer,
):
    yield create_app(given_application_container)


@pytest.fixture
def given_service(
    given_sensor_container: SensorContainer,
) -> SensorRecordService:
    return given_sensor_container.service()


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


@pytest.fixture
async def given_test_client(given_fastapi_app: FastAPI, given_tank: WaterTank):
    async with AsyncClient(
        transport=ASGITransport(given_fastapi_app), base_url="http://test"
    ) as client:
        yield client
