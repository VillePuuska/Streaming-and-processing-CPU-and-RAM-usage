CREATE TABLE postgres_sink (
    `machine_id` INT,
    `measurement_name` STRING,
    `avg_value` DOUBLE,
    `count_value` INT,
    `min_value` DOUBLE,
    `max_value` DOUBLE,
    `window_start` TIMESTAMP,
    `window_time` TIMESTAMP,
    PRIMARY KEY (`machine_id`, `measurement_name`, `window_start`, `window_time`) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://localhost:5432/',
    'table-name' = 'measurements',
    'username' = 'postgres',
    'password' = 'postgres'
);
