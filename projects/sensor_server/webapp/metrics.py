from prometheus_client import Gauge

# 탱크 코드별 센서 기록 카운터 게이지 정의
tank_sensor_records = Gauge(
    "sensor_tank_records_total", "Number of sensor records by tank code", ["tank_code"]
)
