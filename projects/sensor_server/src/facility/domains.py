from dataclasses import dataclass


@dataclass
class WaterTank:
    """수조에 대한 primary key 테이블"""

    tank_id: int  # primary key
    tank_name: str  # 수조 이름
    tank_code: str  # 수조 코드, 외부에서 호출 시 사용 ( unique )

    center_id: int  # center id
    building_id: int  # building id

    @staticmethod
    def new(tank_name: str, building: "WaterTankBuilding") -> "WaterTank":
        return WaterTank(
            tank_id=None,  # 생성 시 자동 생성
            tank_name=tank_name,
            tank_code=f"{building.building_code}_{tank_name}",
            building_id=building.building_id,
            center_id=building.center_id,
        )


@dataclass
class WaterTankBuilding:
    """동에 대한 primary 테이블"""

    building_id: int  # primary key
    building_name: str  # 동 이름
    building_code: str  # 동 코드, 외부에서 호출 시 사용 ( unique )

    center_id: int  # 소속된 center id

    @staticmethod
    def new(building_name: str, center: "WaterTankCenter") -> "WaterTankBuilding":
        return WaterTankBuilding(
            building_id=None,  # 생성 시 자동 생성
            building_name=building_name,
            building_code=f"{center.center_id}_{building_name}",
            center_id=center.center_id,
        )


@dataclass
class WaterTankCenter:
    """센터에 대한 primary key 테이블"""

    center_id: int  # primary key
    center_name: str  # 센터 이름

    @staticmethod
    def new(center_name: str) -> "WaterTankCenter":
        return WaterTankCenter(
            center_id=None,  # 생성 시 자동 생성
            center_name=center_name,
        )
