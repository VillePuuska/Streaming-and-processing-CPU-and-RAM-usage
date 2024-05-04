from confluent_kafka.admin import AdminClient


def check_topic_exists(topic: str, broker: str) -> bool:
    admin = AdminClient({"bootstrap.servers": broker})
    topic_dict = admin.list_topics().topics
    return topic in topic_dict
