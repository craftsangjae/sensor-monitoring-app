import logging

from sqlalchemy import (
    Column,
    VARCHAR,
    Integer,
)

from src.facility.domains import (
    WaterTank,
    WaterTankBuilding,
    WaterTankCenter,
)
from src.database.base import Base

logger = logging.getLogger(__name__)


class WaterTankEntity(Base):
    """수조 정보 저장"""

    __tablename__ = "water_tank"

    tank_id = Column(Integer, primary_key=True, autoincrement=True)  # 수조 id
    tank_name = Column(VARCHAR(20))  # 수조 이름
    tank_code = Column(VARCHAR(64), unique=True)  # 수조 코드

    center_id = Column(Integer)  # 소속된 center id
    building_id = Column(Integer)  # 소속된 building id

    @staticmethod
    def from_domain(domain: WaterTank):
        """도메인 객체를 엔티티로 변환합니다."""
        return WaterTankEntity(
            tank_id=domain.tank_id,
            tank_name=domain.tank_name,
            tank_code=domain.tank_code,
            center_id=domain.center_id,
            building_id=domain.building_id,
        )

    def to_domain(self) -> WaterTank:
        """엔티티 객체를 도메인 객체로 변환합니다."""
        return WaterTank(
            tank_id=self.tank_id,
            tank_name=self.tank_name,
            tank_code=self.tank_code,
            center_id=self.center_id,
            building_id=self.building_id,
        )

    def update(self, domain: WaterTank):
        """도메인 객체로 엔티티의 값을 업데이트합니다."""
        self.tank_name = domain.tank_name
        self.tank_code = domain.tank_code

    def primary_key(self) -> int:
        """엔티티의 기본 키를 반환합니다."""
        return self.tank_id


class WaterTankBuildingEntity(Base):
    """동 정보 저장"""

    __tablename__ = "water_tank_building"

    building_id = Column(Integer, primary_key=True, autoincrement=True)  # 동 id
    building_name = Column(VARCHAR(20))  # 동 이름
    building_code = Column(VARCHAR(42), unique=True)  # 동 코드

    center_id = Column(Integer)  # 소속된 center id

    @staticmethod
    def from_domain(domain: WaterTankBuilding):
        """도메인 객체를 엔티티로 변환합니다."""
        return WaterTankBuildingEntity(
            building_id=domain.building_id,
            building_name=domain.building_name,
            building_code=domain.building_code,
            center_id=domain.center_id,
        )

    def to_domain(self) -> WaterTankBuilding:
        """엔티티 객체를 도메인 객체로 변환합니다."""
        return WaterTankBuilding(
            building_id=self.building_id,
            building_name=self.building_name,
            building_code=self.building_code,
            center_id=self.center_id,
        )

    def update(self, domain: WaterTankBuilding):
        """도메인 객체로 엔티티의 값을 업데이트합니다."""
        self.building_name = domain.building_name
        self.building_code = domain.building_code

    def primary_key(self) -> int:
        """엔티티의 기본 키를 반환합니다."""
        return self.building_id


class WaterTankCenterEntity(Base):
    """센터 정보 저장"""

    __tablename__ = "water_tank_center"

    center_id = Column(Integer, primary_key=True, autoincrement=True)  # 센터 id
    center_name = Column(VARCHAR(20))  # 센터 이름

    @staticmethod
    def from_domain(domain: WaterTankCenter):
        """도메인 객체를 엔티티로 변환합니다."""
        return WaterTankCenterEntity(
            center_id=domain.center_id,
            center_name=domain.center_name,
        )

    def to_domain(self) -> WaterTankCenter:
        """엔티티 객체를 도메인 객체로 변환합니다."""
        return WaterTankCenter(
            center_id=self.center_id,
            center_name=self.center_name,
        )

    def update(self, domain: WaterTankCenter):
        """도메인 객체로 엔티티의 값을 업데이트합니다."""
        self.center_name = domain.center_name

    def primary_key(self) -> int:
        """엔티티의 기본 키를 반환합니다."""
        return self.center_id
