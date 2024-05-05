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

CREATE OR REPLACE VIEW latest_measurements AS (
    WITH last_time AS (
        SELECT
            machine_id,
            measurement_name,
            MAX(window_time) AS window_time
        FROM measurements
        GROUP BY
            machine_id,
            measurement_name
    )
    SELECT m.*
    FROM measurements m
    INNER JOIN last_time l
    ON m.machine_id = l.machine_id
    AND m.measurement_name = l.measurement_name
    AND m.window_time = l.window_time
);

CREATE OR REPLACE VIEW measurements_last_minute AS (
    SELECT *
    FROM measurements
    WHERE window_time >= now() - INTERVAL '1 minute' -- only the last minute
);
