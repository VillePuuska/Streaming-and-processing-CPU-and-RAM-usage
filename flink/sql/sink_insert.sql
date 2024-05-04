INSERT INTO postgres_sink
    SELECT
        `machine_id`,
        `measurement_name`,
        AVG(`value`) AS `avg`,
        `window_start`,
        `window_time`
    FROM TABLE(
        TUMBLE(TABLE kafka_feed, DESCRIPTOR(ts), INTERVAL '1' SECONDS)
    )
    GROUP BY
        `machine_id`,
        `measurement_name`,
        `window_start`,
        `window_time`;
