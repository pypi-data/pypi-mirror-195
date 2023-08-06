"kafka api"
from confluent_kafka import Consumer, KafkaException, Message, KafkaError, TIMESTAMP_NOT_AVAILABLE
from confluent_kafka import TopicPartition, OFFSET_BEGINNING, OFFSET_END
from confluent_kafka.admin import AdminClient, ClusterMetadata, TopicMetadata

import requests # type: ignore

from dwh_oppfolging.apis.secrets_api_v1 import get_kafka_secrets_for_topic


def is_dwh_consumer_alive(name: str):
    """returns true if dwh-consumer isalive endpoint returns OK"""
    # pylint: disable=no-member
    return requests.get("https://" + name + ".nais.adeo.no/isalive", timeout=10).status_code == requests.codes.ok


def consume_messages_from_topic(topic: str):
    # key, ca, cerfiticate
    raise NotImplementedError
