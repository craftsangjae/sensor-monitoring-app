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
        recorded_at TIMESTAMP WITH TIME ZONE NOT NULL, 

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
        recorded_at TIMESTAMP WITH TIME ZONE NOT NULL, 

        FOREIGN KEY (tank_id) REFERENCES water_tank(tank_id)
);

-- 하이퍼테이블로 변환
SELECT create_hypertable('water_tank_sensor_record_history', 'recorded_at');
CREATE INDEX ON water_tank_sensor_record_history_tank_id_recorded_at_idx (tank_id, recorded_at DESC);

-- 데이터 넣기
INSERT INTO water_tank_center (center_id, center_name) VALUES (1, '임실');
INSERT INTO water_tank_center (center_id, center_name) VALUES (2, '정읍');

INSERT INTO water_tank_building (building_id, building_name, building_code, center_id) VALUES (1, '제1동', '임실_제1동', 1);
INSERT INTO water_tank_building (building_id, building_name, building_code, center_id) VALUES (2, '제2동', '임실_제2동', 1);
INSERT INTO water_tank_building (building_id, building_name, building_code, center_id) VALUES (3, '제3동', '임실_제3동', 1);
INSERT INTO water_tank_building (building_id, building_name, building_code, center_id) VALUES (4, '제4동', '임실_제4동', 1);

INSERT INTO water_tank_building (building_id, building_name, building_code, center_id) VALUES (5, '제1동', '정읍_제1동', 2);
INSERT INTO water_tank_building (building_id, building_name, building_code, center_id) VALUES (6, '제2동', '정읍_제2동', 2);
INSERT INTO water_tank_building (building_id, building_name, building_code, center_id) VALUES (7, '제3동', '정읍_제3동', 2);
INSERT INTO water_tank_building (building_id, building_name, building_code, center_id) VALUES (8, '제4동', '정읍_제4동', 2);

INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (1, '제1탱크', '임실_제1동_제1탱크', 1, 1);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (2, '제2탱크', '임실_제1동_제2탱크', 1, 1);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (3, '제3탱크', '임실_제1동_제3탱크', 1, 1);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (4, '제4탱크', '임실_제1동_제4탱크', 1, 1);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (5, '제5탱크', '임실_제1동_제5탱크', 1, 1);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (6, '제6탱크', '임실_제1동_제6탱크', 1, 1);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (7, '제7탱크', '임실_제1동_제7탱크', 1, 1);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (8, '제8탱크', '임실_제1동_제8탱크', 1, 1);

INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (9, '제1탱크', '임실_제2동_제1탱크', 1, 2);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (10, '제2탱크', '임실_제2동_제2탱크', 1, 2);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (11, '제3탱크', '임실_제2동_제3탱크', 1, 2);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (12, '제4탱크', '임실_제2동_제4탱크', 1, 2);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (13, '제5탱크', '임실_제2동_제5탱크', 1, 2);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (14, '제6탱크', '임실_제2동_제6탱크', 1, 2);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (15, '제7탱크', '임실_제2동_제7탱크', 1, 2);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (16, '제8탱크', '임실_제2동_제8탱크', 1, 2);

INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (17, '제1탱크', '임실_제3동_제1탱크', 1, 3);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (18, '제2탱크', '임실_제3동_제2탱크', 1, 3);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (19, '제3탱크', '임실_제3동_제3탱크', 1, 3);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (20, '제4탱크', '임실_제3동_제4탱크', 1, 3);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (21, '제5탱크', '임실_제3동_제5탱크', 1, 3);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (22, '제6탱크', '임실_제3동_제6탱크', 1, 3);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (23, '제7탱크', '임실_제3동_제7탱크', 1, 3);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (24, '제8탱크', '임실_제3동_제8탱크', 1, 3);

INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (25, '제1탱크', '임실_제4동_제1탱크', 1, 4);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (26, '제2탱크', '임실_제4동_제2탱크', 1, 4);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (27, '제3탱크', '임실_제4동_제3탱크', 1, 4);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (28, '제4탱크', '임실_제4동_제4탱크', 1, 4);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (29, '제5탱크', '임실_제4동_제5탱크', 1, 4);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (30, '제6탱크', '임실_제4동_제6탱크', 1, 4);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (31, '제7탱크', '임실_제4동_제7탱크', 1, 4);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (32, '제8탱크', '임실_제4동_제8탱크', 1, 4);

INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (33, '제1탱크', '정읍_제1동_제1탱크', 2, 5);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (34, '제2탱크', '정읍_제1동_제2탱크', 2, 5);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (35, '제3탱크', '정읍_제1동_제3탱크', 2, 5);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (36, '제4탱크', '정읍_제1동_제4탱크', 2, 5);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (37, '제5탱크', '정읍_제1동_제5탱크', 2, 5);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (38, '제6탱크', '정읍_제1동_제6탱크', 2, 5);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (39, '제7탱크', '정읍_제1동_제7탱크', 2, 5);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (40, '제8탱크', '정읍_제1동_제8탱크', 2, 5);

INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (41, '제1탱크', '정읍_제2동_제1탱크', 2, 6);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (42, '제2탱크', '정읍_제2동_제2탱크', 2, 6);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (43, '제3탱크', '정읍_제2동_제3탱크', 2, 6);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (44, '제4탱크', '정읍_제2동_제4탱크', 2, 6);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (45, '제5탱크', '정읍_제2동_제5탱크', 2, 6);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (46, '제6탱크', '정읍_제2동_제6탱크', 2, 6);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (47, '제7탱크', '정읍_제2동_제7탱크', 2, 6);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (48, '제8탱크', '정읍_제2동_제8탱크', 2, 6);

INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (49, '제1탱크', '정읍_제3동_제1탱크', 2, 7);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (50, '제2탱크', '정읍_제3동_제2탱크', 2, 7);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (51, '제3탱크', '정읍_제3동_제3탱크', 2, 7);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (52, '제4탱크', '정읍_제3동_제4탱크', 2, 7);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (53, '제5탱크', '정읍_제3동_제5탱크', 2, 7);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (54, '제6탱크', '정읍_제3동_제6탱크', 2, 7);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (55, '제7탱크', '정읍_제3동_제7탱크', 2, 7);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (56, '제8탱크', '정읍_제3동_제8탱크', 2, 7);

INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (57, '제1탱크', '정읍_제4동_제1탱크', 2, 8);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (58, '제2탱크', '정읍_제4동_제2탱크', 2, 8);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (59, '제3탱크', '정읍_제4동_제3탱크', 2, 8);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (60, '제4탱크', '정읍_제4동_제4탱크', 2, 8);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (61, '제5탱크', '정읍_제4동_제5탱크', 2, 8);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (62, '제6탱크', '정읍_제4동_제6탱크', 2, 8);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (63, '제7탱크', '정읍_제4동_제7탱크', 2, 8);
INSERT INTO water_tank (tank_id, tank_name, tank_code, center_id, building_id) VALUES (64, '제8탱크', '정읍_제4동_제8탱크', 2, 8);









