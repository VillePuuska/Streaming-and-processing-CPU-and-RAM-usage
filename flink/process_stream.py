import click
import os

from pyflink.table import EnvironmentSettings, TableEnvironment  # type: ignore


@click.command()
@click.option(
    "--jar-path",
    type=str,
    default="/workspaces/Streaming-and-processing-CPU-and-RAM-usage/jars",
    help="""Path to the jars Flink needs. MUST BE ABSOLUTE. See `flink/needed_jar_urls.txt` for a list of needed jars.
    Default: /workspaces/Streaming-and-processing-CPU-and-RAM-usage/jars""",
)
@click.option(
    "--kafka-ddl-path",
    type=str,
    default="flink/sql/kafka_ddl.sql",
    help="Path to the DDL Flink needs to read the Kafka topic. Default: flink/sql/kafka_ddl.sql",
)
@click.option(
    "--postgres-ddl-path",
    type=str,
    default="flink/sql/postgres_ddl.sql",
    help="""Path to the DDL Flink needs to sink the stream to the Postgres/Timescale table.
    Default: flink/sql/postgres_ddl.sql""",
)
@click.option(
    "--sink-query-path",
    type=str,
    default="flink/sql/sink_insert.sql",
    help="""Path to the INSERT INTO ... SELECT ... statement that defines the stream processing and
    the sink. Default: flink/sql/sink_insert.sql""",
)
def process(
    jar_path: str,
    kafka_ddl_path: str,
    postgres_ddl_path: str,
    sink_query_path: str,
):
    t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
    t_env.get_config().set("parallelism.default", "1")

    jars = [
        "flink-sql-avro-1.18.0.jar",
        "flink-sql-avro-confluent-registry-1.18.0.jar",
        "flink-sql-connector-kafka-3.1.0-1.18.jar",
        "flink-connector-jdbc-3.1.2-1.18.jar",
        "postgresql-42.7.3.jar",
    ]
    jar_paths = ["file://" + os.path.join(jar_path, jar) for jar in jars]
    missing_jars = [path[7:] for path in jar_paths if not os.path.isfile(path[7:])]
    if len(missing_jars) > 0:
        raise Exception(
            f"The given jar-path is missing the following jars: {'; '.join(missing_jars)}"
        )
    t_env.get_config().set("pipeline.jars", ";".join(jar_paths))

    with open(kafka_ddl_path) as f:
        kafka_topic_ddl = f.read()

    with open(postgres_ddl_path) as f:
        postgres_sink_ddl = f.read()

    with open(sink_query_path) as f:
        sink_query = f.read()

    t_env.execute_sql(kafka_topic_ddl)
    t_env.execute_sql(postgres_sink_ddl)
    t_env.execute_sql(sink_query).wait()


if __name__ == "__main__":
    process()
