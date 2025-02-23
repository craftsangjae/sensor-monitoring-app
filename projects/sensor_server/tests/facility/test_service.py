import pytest

from src.facility.container import FacilityContainer
from src.facility.domains import WaterTank, WaterTankBuilding, WaterTankCenter
from src.facility.repository import (
    WaterTankBuildingRepository,
    WaterTankCenterRepository,
    WaterTankRepository,
)
from src.facility.service import FacilityService


@pytest.fixture
def given_service(
    given_facility_container: FacilityContainer,
):
    return given_facility_container.service()


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
    given_center: WaterTankCenter,
):
    """테스트용 수조 생성"""
    tank = WaterTank.new(
        tank_name="test_tank", building=given_building, center=given_center
    )
    await given_water_tank_repository.save(tank)
    return tank


async def test_tank_get_by_code(
    given_tank: WaterTank,
    given_service: FacilityService,
):
    """테스트용 수조 생성"""
    tank = await given_service.get_water_tank_by_code(given_tank.tank_code)

    assert tank is not None
    assert tank.tank_id == given_tank.tank_id
    assert tank.tank_name == given_tank.tank_name
    assert tank.building_id == given_tank.building_id
