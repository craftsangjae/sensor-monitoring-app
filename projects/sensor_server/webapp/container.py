from dependency_injector import containers, providers
from src.database.container import DatabaseContainer
from src.facility.container import FacilityContainer
from src.sensor.container import SensorContainer
from webapp.logger import initialize_logger
import logging

logger = logging.getLogger(__name__)


class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["webapp"])

    logger = providers.Resource(initialize_logger)

    database: DatabaseContainer = providers.Container(DatabaseContainer)

    facility: FacilityContainer = providers.Container(
        FacilityContainer,
        database=database,
    )

    sensor: SensorContainer = providers.Container(
        SensorContainer,
        database=database,
        facility=facility,
    )


def preload_dependency(container: ApplicationContainer):
    """
    첫 API의 응답성이 느리게 나오는 것을 방지하기 위해, 의존성 초기화를 미리 진행.

    TODO: dependency injector에서는 컨테이너 초기화 시 preloading하는 기능을 제공하지 않는다.
          향후 보다 간단하게 처리할 수 있는 방법을 모색할 필요가 있다.
    """
    try:
        logger.info("Preloading dependencies...")
        container.sensor.service()
        container.facility.service()
        logger.info("Preloading dependencies... done")
    except Exception as e:
        logger.error(f"Failed to preload container: {e}")


def create_container() -> ApplicationContainer:
    container = ApplicationContainer()

    # 리소스 (logger) 초기화
    container.init_resources()

    # 의존성 초기화
    preload_dependency(container)
    return container
