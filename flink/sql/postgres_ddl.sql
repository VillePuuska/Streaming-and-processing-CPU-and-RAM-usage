CREATE TABLE postgres_sink (
    `machine_id` INT,
    `measurement_name` STRING,
    `avg` DOUBLE,
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
