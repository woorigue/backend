from typing import Final
import pika
from .config import settings
from pika.exchange_type import ExchangeType


class RabbitBase:
    """
    Setup default setting of rabbitmq server
    """

    TOPIC_EXCHANGE: Final[str] = "amq.topic"
    NOTICE_EXCHANGE: Final[str] = "amq.fanout"

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(settings.RABBITMQ_URL)
        )
        self.channel = self.connection.channel()

        # default setup methods
        self._setup_exchange()

    def _setup_exchange(self):
        # setup topic exchange
        self.channel.exchange_declare(
            exchange=self.TOPIC_EXCHANGE,
            exchange_type=ExchangeType.topic,
            durable=True,
        )

        # setup topic exchange
        self.channel.exchange_declare(
            exchange=self.NOTICE_EXCHANGE,
            exchange_type=ExchangeType.fanout,
            durable=True,
        )


class RabbitHelper(RabbitBase):
    def publish(self, chat_room, message, user_id):
        routing_key = f"user.1.chat.10"
        # self.channel.queue_declare(queue="messages2", durable=True)
        # self.channel.queue_bind(
        #     exchange=self.TOPIC_EXCHANGE, queue="messages2", routing_key=routing_key
        # )
        routing_key = f"user.1.chat.10"
        self.channel.basic_publish(
            exchange=self.TOPIC_EXCHANGE, routing_key=routing_key, body=message
        )
