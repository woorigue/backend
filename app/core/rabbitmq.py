import pika


class RabbitMQClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters("amqp://guest:guest@52.79.239.1/")
        )
        self.channel = self.connection.channel()
        self.exchange_name = "amq.topic"

    def publish_message(self, message, route_key):
        self.channel.queue_declare(queue="users")  # 큐 생성(선언)
        self.channel.queue_bind(  # 큐 바인딩(mapping)
            exchange=self.exchange_name, queue="users", routing_key="users.1.#"
        )
        self.channel.basic_publish(
            exchange=self.exchange_name, routing_key=route_key, body=message
        )
