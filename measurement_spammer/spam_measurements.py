from utils.readings import get_readings
from utils.kafka_helpers import check_topic_exists
import time
import click

from confluent_kafka import KafkaException, Producer
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
    IntegerSerializer,
)


@click.command()
@click.option(
    "--interval",
    type=float,
    default=0.3,
    help="""Interval for how often to send a measurement to Kafka.
    For example, setting `--interval 1.0` sends a measurement every second.
    Default: 0.3""",
)
@click.option(
    "--topic",
    type=str,
    default="measurements",
    help="""Kafka topic to send measurements to.
    Default: measurements""",
)
@click.option(
    "--allow-new-topic/--disallow-new-topic",
    default=False,
    help="""Flag for (dis)allowing the script to create a new topic if the specified topic does not yet exist.
    Default: disallow""",
)
@click.option(
    "--machine-id",
    type=int,
    default=1,
    help="""The `machine_id` in the records sent to Kafka.
    Default: 1""",
)
@click.option(
    "--schema-path",
    type=str,
    default="avro/schema.avsc",
    help="""Path to the AVRO schema file. Can be relative or absolute.
    Default: avro/schema.avsc""",
)
@click.option(
    "--broker",
    type=str,
    default="localhost:9092",
    help="""Kafka bootstrap servers.
    Default: localhost:9092""",
)
@click.option(
    "--schema-registry",
    type=str,
    default="http://localhost:8081",
    help="""URL to the schema registry.
    Default: http://localhost:8081""",
)
def spam(
    interval: float,
    topic: str,
    allow_new_topic: bool,
    machine_id: int,
    schema_path: str,
    broker: str,
    schema_registry: str,
):
    """
    Script to send CPU and RAM usage measurements to a specified Kafka topic.
    """

    if not allow_new_topic and not check_topic_exists(topic=topic, broker=broker):
        raise Exception(
            "Topic does not exist. Set `--allow-new-topic` if you want the script to create the topic."
        )

    schema_registry_client = SchemaRegistryClient({"url": schema_registry})

    with open(schema_path) as f:
        schema = Schema(f.read(), "AVRO")

    serializer = AvroSerializer(schema_registry_client, schema)
    key_serializer = IntegerSerializer()

    producer = Producer({"bootstrap.servers": broker})

    try:
        prev_time = time.time()
        while True:
            timestamp = int(time.time() * 1000)
            readings = get_readings()

            for k, v in readings.items():
                message = {
                    "machine_id": machine_id,
                    "measurement_timestamp": timestamp,
                    "measurement_name": k,
                    "value": v,
                }

                producer.produce(
                    topic=topic,
                    key=key_serializer(
                        machine_id,
                        SerializationContext(topic, MessageField.KEY),
                    ),
                    value=serializer(
                        message,
                        SerializationContext(topic, MessageField.VALUE),
                    ),
                )
                producer.flush()
                print(f"Record: {message}")

            time.sleep(max(0, prev_time + interval - time.time()))
            prev_time += interval
    except KafkaException as e:
        print(f"Caught a Kafka Exception:\n{e}")
    except KeyboardInterrupt:
        print("Stopping producing readings.")


if __name__ == "__main__":
    spam()
