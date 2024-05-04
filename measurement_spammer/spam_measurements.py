from utils.readings import get_readings
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

MACHINE_ID = 1
SCHEMA_PATH = "avro/schema.avsc"
KAFKA_CONN = "localhost:9092"
SCHEMA_REGISTRY_CONN = "http://localhost:8081"


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
def spam(interval: float, topic: str):
    """
    Script to send CPU and RAM usage measurements to a specified Kafka topic.
    """
    schema_registry_client = SchemaRegistryClient({"url": SCHEMA_REGISTRY_CONN})

    with open(SCHEMA_PATH) as f:
        schema = Schema(f.read(), "AVRO")

    serializer = AvroSerializer(schema_registry_client, schema)
    key_serializer = IntegerSerializer()

    producer = Producer({"bootstrap.servers": KAFKA_CONN})

    try:
        prev_time = time.time()
        while True:
            timestamp = int(time.time() * 1000)
            readings = get_readings()

            for k, v in readings.items():
                message = {
                    "machine_id": MACHINE_ID,
                    "measurement_timestamp": timestamp,
                    "measurement_name": k,
                    "value": v,
                }

                producer.produce(
                    topic=topic,
                    key=key_serializer(
                        MACHINE_ID,
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
