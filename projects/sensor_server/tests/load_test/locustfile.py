from locust import TaskSet, task, constant
from locust.contrib.fasthttp import FastHttpUser
import random
import asyncio
from datetime import datetime
from typing import List


class AsyncSensorRecordBehavior(TaskSet):
    def on_start(self):
        self.locations = ["임실", "정읍"]
        self.buildings = [f"제{i}동" for i in range(1, 5)]
        self.tank_numbers = [f"제{i}탱크" for i in range(1, 9)]

        self.tank_codes = [
            f"{loc}_{bld}_{tnk}"
            for loc in self.locations
            for bld in self.buildings
            for tnk in self.tank_numbers
        ]

    def generate_sensor_data(self, tank_codes: List[str]) -> List[dict]:
        """센서 데이터 생성"""
        return [
            {
                "tank_code": tank_code,
                "temperature": round(random.uniform(20.0, 30.0), 1),
                "ph": round(random.uniform(6.5, 8.5), 1),
                "salinity": round(random.uniform(10.0, 30.0), 1),
                "dissolved_oxygen": round(random.uniform(10.0, 30.0), 1),
                "recorded_at": int(datetime.now().timestamp()),
            }
            for tank_code in tank_codes
        ]

    @task
    def record_all_tank_sensors(self):
        """모든 탱크의 센서 데이터 전송"""
        sensor_data = self.generate_sensor_data(self.tank_codes)

        for payload in sensor_data:
            self.client.post(
                "/api/records/water-tank-sensor",
                json=payload,
                name=f"Record Tank Sensor/{payload['tank_code'].split('_')[0]}",
            )


class SensorUser(FastHttpUser):
    tasks = [AsyncSensorRecordBehavior]
    wait_time = constant(1)
    host = "https://sensor.crafthomelab.com"
