from utils.readings import get_readings
import time

from confluent_kafka import KafkaException, Producer
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
    IntegerSerializer,
)

TIMEDELTA = 0.3
TOPIC = "measurements"
MACHINE_ID = 1
SCHEMA_PATH = "avro/schema.avsc"
KAFKA_CONN = "localhost:9092"
SCHEMA_REGISTRY_CONN = "http://localhost:8081"


def main():
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
                    topic=TOPIC,
                    key=key_serializer(MACHINE_ID, MessageField.KEY),
                    value=serializer(
                        message,
                        SerializationContext(TOPIC, MessageField.VALUE),
                    ),
                )
                producer.flush()
                print(f"Record: {message}")

            time.sleep(max(0, prev_time + TIMEDELTA - time.time()))
            prev_time += TIMEDELTA
    except KafkaException as e:
        print(f"Caught a Kafka Exception:\n{e}")
    except KeyboardInterrupt:
        print("Stopping producing readings.")


if __name__ == "__main__":
    main()
