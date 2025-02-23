import logging

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
)

from src.sensor.domains import WaterTankSensorRecord
from src.database.base import Base

logger = logging.getLogger(__name__)


class WaterTankSensorRecordEntity(Base):
    """수조 센서 측정 값 저장"""

    __tablename__ = "water_tank_sensor_record"

    tank_id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    ph = Column(Float)
    recorded_at = Column(DateTime)

    @staticmethod
    def from_domain(domain: WaterTankSensorRecord):
        """도메인 객체를 엔티티로 변환합니다."""
        return WaterTankSensorRecordEntity(
            tank_id=domain.tank_id,
            temperature=domain.temperature,
            ph=domain.ph,
            recorded_at=domain.recorded_at,
        )

    def to_domain(self) -> WaterTankSensorRecord:
        """엔티티 객체를 도메인 객체로 변환합니다."""
        return WaterTankSensorRecord(
            tank_id=self.tank_id,
            temperature=self.temperature,
            ph=self.ph,
            recorded_at=self.recorded_at,
        )

    def update(self, domain: WaterTankSensorRecord):
        """도메인 객체로 엔티티의 값을 업데이트합니다."""
        self.temperature = domain.temperature
        self.ph = domain.ph

    def primary_key(self) -> int:
        """엔티티의 기본 키를 반환합니다."""
        return self.tank_id


class WaterTankSensorRecordHistoryEntity(Base):
    """수조 센서 측정 값 저장"""

    __tablename__ = "water_tank_sensor_record_history"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    tank_id = Column(Integer)
    temperature = Column(Float)
    ph = Column(Float)
    recorded_at = Column(DateTime)

    @staticmethod
    def from_domain(domain: WaterTankSensorRecord):
        """도메인 객체를 엔티티로 변환합니다."""
        return WaterTankSensorRecordHistoryEntity(
            tank_id=domain.tank_id,
            temperature=domain.temperature,
            ph=domain.ph,
            recorded_at=domain.recorded_at,
        )

    def to_domain(self) -> WaterTankSensorRecord:
        """엔티티 객체를 도메인 객체로 변환합니다."""
        return WaterTankSensorRecord(
            tank_id=self.tank_id,
            temperature=self.temperature,
            ph=self.ph,
            recorded_at=self.recorded_at,
        )

    def update(self, domain: WaterTankSensorRecord):
        """도메인 객체로 엔티티의 값을 업데이트합니다."""
        self.temperature = domain.temperature
        self.ph = domain.ph

    def primary_key(self) -> int:
        """엔티티의 기본 키를 반환합니다."""
        return self.tank_id
