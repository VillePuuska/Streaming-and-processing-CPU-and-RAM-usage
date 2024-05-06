INSERT INTO postgres_sink
    SELECT
        `machine_id`,
        `measurement_name`,
        AVG(`value`) AS `avg_value`,
        CAST(COUNT(`value`) AS INT) AS `count_value`,
        MIN(`value`) AS `min_value`,
        MAX(`value`) AS `max_value`,
        `window_start`,
        `window_time`
    FROM TABLE(
        TUMBLE(TABLE kafka_feed, DESCRIPTOR(measurement_timestamp), INTERVAL '1' SECONDS)
    )
    GROUP BY
        `machine_id`,
        `measurement_name`,
        `window_start`,
        `window_time`;
