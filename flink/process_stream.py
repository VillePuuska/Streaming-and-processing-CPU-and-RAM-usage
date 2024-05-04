import click
from pyflink.table import EnvironmentSettings, TableEnvironment  # type: ignore


@click.command()
def process():
    t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
    t_env.get_config().set("parallelism.default", "1")

    jar_dir = "/workspaces/Streaming-and-processing-CPU-and-RAM-usage/jars/"
    jars = [
        "flink-sql-avro-1.18.0.jar",
        "flink-sql-avro-confluent-registry-1.18.0.jar",
        "flink-sql-connector-kafka-3.1.0-1.18.jar",
        "flink-connector-jdbc-3.1.2-1.18.jar",
        "postgresql-42.7.3.jar",
    ]
    jar_paths = ["file://" + jar_dir + jar for jar in jars]
    t_env.get_config().set("pipeline.jars", ";".join(jar_paths))

    kafka_topic_ddl = f"""
    CREATE TABLE kafka_feed (
        `machine_id` INT,
        `measurement_name` STRING,
        `value` DOUBLE,
        `ts` TIMESTAMP(3) METADATA FROM 'timestamp',
        WATERMARK FOR `ts` AS `ts`
    ) with (
        'connector' = 'kafka',
        'topic' = 'measurements',
        'properties.bootstrap.servers' = 'localhost:9092',
        'properties.group.id' = 'flinkgroup',
        'scan.startup.mode' = 'latest-offset',
        'value.format' = 'avro-confluent',
        'value.avro-confluent.url' = 'http://localhost:8081'
    )
    """

    postgres_sink_ddl = f"""
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
    )
    """

    sink_query = f"""
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
            `window_time`
    """

    t_env.execute_sql(kafka_topic_ddl)
    t_env.execute_sql(postgres_sink_ddl)
    t_env.execute_sql(sink_query).wait()


if __name__ == "__main__":
    process()
