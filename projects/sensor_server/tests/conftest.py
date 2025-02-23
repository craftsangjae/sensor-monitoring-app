import pytest
from src.database.container import DatabaseContainer
from src.database.settings import DatabaseSettings
from src.sensor.container import SensorContainer
from src.facility.container import FacilityContainer
from testcontainers.postgres import PostgresContainer

import logging
from pathlib import Path

RESOURCE_DIR = Path(__file__).parent / "resources"


@pytest.fixture(scope="session")
def initialize_test_logger():
    """테스트 로거 초기화"""
    logger = logging.getLogger()
    logger.setLevel("INFO")
    logger.propagate = False
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(levelname)5s][%(filename)s:%(lineno)s] %(message)s",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@pytest.fixture(scope="session")
def event_loop(initialize_test_logger):
    """
    테스트 과정 중 사용할 이벤트 루프가 모두 동일한 이벤트 루프를 이용하도록 설정합니다.

    [pytest-asyncio 시 지정이 필요한 부분]

        1. 비동기 테스트 함수 위에 @pytest.mark.asyncio(loop_scope="session") 추가
        2. pyproject.toml 파일에 아래 내용 추가 (asyncio_default_fixture_loop_scope = "session", asyncio_mode = "auto")
            [tool.pytest.ini_options]
            minversion = "6.0"
            asyncio_mode = "auto"
            asyncio_default_fixture_loop_scope = "session"

    [ 추가하는 이유 ]
    위 지정이 누락되어 있는 경우, 테스트 시 sqlalchemy에서 different event loop exception이 발생할 수 있습니다.
    해당 에러가 발생하는 이유를 추측하자면, pytest.fixture 내에서 setup 시 sqlalchemy에서 사용하는 이벤트 루프가 별개로 생성되어 발생하는 것으로 보입니다.
    """
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def pytest_collection_modifyitems(items):
    """
    pytest-asyncio 테스트 함수에 loop_scope="session" 마커를 추가합니다.
    - 모두 event loop을 공유하도록 하여, 테스트 함수 간에 different event loop exception이 발생하지 않도록 합니다.

    reference: https://pytest-asyncio.readthedocs.io/en/stable/how-to-guides/run_session_tests_in_same_loop.html
    """
    from pytest_asyncio import is_async_test

    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="session")
def given_postgres_container():
    """테스트용 timescale 도커 컨테이너 Instance 생성
    timescale는 postgres에 timescaledb extension을 추가한 것으로, time-series data를 위해 사용합니다.
    """
    with PostgresContainer(
        image="timescale/timescaledb-ha:pg16",
        username="postgres",
        password="password",
        dbname="postgres",
        port=5432,
    ) as timescale_container:
        yield timescale_container


@pytest.fixture(scope="session")
def given_database_settings(given_postgres_container: PostgresContainer):
    """테스트용 database settings 생성"""
    return DatabaseSettings(
        DB_TYPE="postgresql",
        DB_NAME=given_postgres_container.dbname,
        DB_USER=given_postgres_container.username,
        DB_PASSWORD=given_postgres_container.password,
        DB_HOST=given_postgres_container.get_container_host_ip(),
        DB_PORT=given_postgres_container.get_exposed_port(5432),
        DB_ECHO=False,
    )


@pytest.fixture(scope="session")
def given_database_container(given_database_settings: DatabaseSettings):
    """테스트용 database container 생성"""
    return DatabaseContainer(settings=given_database_settings)


@pytest.fixture(scope="session")
def given_facility_container(given_database_container: DatabaseContainer):
    """테스트용 facility container 생성"""
    return FacilityContainer(database=given_database_container)


@pytest.fixture(scope="session")
def given_sensor_container(
    given_database_container: DatabaseContainer,
    given_facility_container: FacilityContainer,
):
    """테스트용 sensor container 생성"""
    return SensorContainer(
        database=given_database_container,
        facility=given_facility_container,
    )


@pytest.fixture
async def initialize_database(given_database_container: DatabaseContainer):
    """테스트용 database 초기화"""
    session_factory = given_database_container.session_factory()
    await session_factory.create_database()
    yield
    await session_factory.drop_database()
