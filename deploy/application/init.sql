-- 수조 센터 테이블
CREATE TABLE water_tank_center (
        center_id SERIAL NOT NULL, 
        center_name VARCHAR(20), 
        PRIMARY KEY (center_id)
)


-- 수조 동 테이블
CREATE TABLE water_tank_building (
        building_id SERIAL NOT NULL, 
        building_name VARCHAR(20), 
        building_code VARCHAR(42), 
        center_id INTEGER, 
        PRIMARY KEY (building_id), 
        UNIQUE (building_code),
        
        FOREIGN KEY (center_id) REFERENCES water_tank_center(center_id)
)

-- 수조 탱크 테이블
CREATE TABLE water_tank (
        tank_id SERIAL NOT NULL, 
        tank_name VARCHAR(20), 
        tank_code VARCHAR(64), 
        center_id INTEGER, 
        building_id INTEGER, 
        PRIMARY KEY (tank_id), 
        UNIQUE (tank_code),
        
        FOREIGN KEY (center_id) REFERENCES water_tank_center(center_id),
        FOREIGN KEY (building_id) REFERENCES water_tank_building(building_id)
);

-- 수조 센서 기록 테이블
CREATE TABLE water_tank_sensor_record(
        tank_id INTEGER NOT NULL, 
        temperature FLOAT, 
        ph FLOAT, 
        dissolved_oxygen FLOAT, 
        salinity FLOAT, 
        recorded_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 

        PRIMARY KEY (tank_id),
        FOREIGN KEY (tank_id) REFERENCES water_tank(tank_id)
);

-- 수조 센서 기록 히스토리 테이블
CREATE TABLE water_tank_sensor_record_history (
        tank_id INTEGER NOT NULL, 
        temperature FLOAT, 
        ph FLOAT, 
        dissolved_oxygen FLOAT,
        salinity FLOAT, 
        recorded_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
        PRIMARY KEY (tank_id, recorded_at),

        FOREIGN KEY (tank_id) REFERENCES water_tank(tank_id)
);
