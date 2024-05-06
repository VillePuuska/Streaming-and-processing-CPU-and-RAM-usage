CREATE TABLE kafka_feed (
    `machine_id` INT,
    `measurement_timestamp` TIMESTAMP(3),
    `measurement_name` STRING,
    `value` DOUBLE,
    -- `ts` TIMESTAMP(3) METADATA FROM 'timestamp',
    -- allow events arriving 1 second late
    WATERMARK FOR `measurement_timestamp` AS `measurement_timestamp` - INTERVAL '1' SECOND
) with (
    'connector' = 'kafka',
    'topic' = 'measurements',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'flinkgroup',
    'scan.startup.mode' = 'latest-offset',
    'value.format' = 'avro-confluent',
    'value.avro-confluent.url' = 'http://localhost:8081'
);
