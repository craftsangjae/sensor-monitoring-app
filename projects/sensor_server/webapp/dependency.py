from typing import Annotated, Optional
from src.sensor.service import SensorRecordService
from webapp.container import ApplicationContainer
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security_scheme = HTTPBearer(auto_error=False)


@inject
def sensor_service_dependency(
    sensor_service: SensorRecordService = Depends(
        Provide[ApplicationContainer.sensor.service]
    ),
) -> SensorRecordService:
    return sensor_service
