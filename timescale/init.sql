DROP TABLE IF EXISTS measurements;

CREATE TABLE measurements (
    machine_id INT,
    measurement_name VARCHAR,
    avg_value FLOAT8,
    count_value INT,
    min_value FLOAT8,
    max_value FLOAT8,
    window_start TIMESTAMPTZ,
    window_time TIMESTAMPTZ,
    PRIMARY KEY (machine_id, measurement_name, window_start, window_time)
);

SELECT create_hypertable('measurements', by_range('window_start', INTERVAL '1 day'));
