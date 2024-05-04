from confluent_kafka.admin import AdminClient
from confluent_kafka import KafkaError


def check_topic_exists(topic: str, broker: str) -> bool:
    admin = AdminClient({"bootstrap.servers": broker})
    topic_dict = admin.list_topics().topics
    return topic in topic_dict


def producer_callback(err: KafkaError | None, _) -> None:
    if err is None:
        return
    print(f"Delivering message failed with the following exception:\n{err}")
