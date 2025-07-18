import os

from pika import BlockingConnection, URLParameters
from pika.channel import Channel

ANSWER_EXCHANGE = 'answer'


def initialize_rabbit_channel():
    url = os.environ.get('AR_RABBIT_URL') or 'amqp://localhost:5672/%2F?heartbeat=300'
    # FIXME connection should be init one time per thread (use singleton pattern)
    conn = BlockingConnection(URLParameters(url))
    chan = conn.channel()
    chan.exchange_declare(exchange=ANSWER_EXCHANGE, exchange_type='topic')
    return chan


def safe_publish(chan: Channel | None, exchange_name: str, routing_key: str, body) -> Channel:
    """
    Attempts to send message via rabbit. Ensures channel is open before sending and opens a new channel if necessary.

    :param chan: channel to use for publishing. If None or closed, a new channel will be created.
    :param exchange_name: name of exchange to publish to
    :param routing_key: this is currently only for answer updates, so use one of:
        <id>.chat for raw chat messages. a subscription listens for this to update the chat panel in the ui
        <id>.artifact for artifact updates notifications. a subscription listens for this to update the artifacts panel
        <id>.complete to notify about answer completion.
        for general info see https://www.rabbitmq.com/docs/exchanges#topic
    :param body: message to publish

    NOTE: use the returned channel for future publishes to reduce connection overhead.

    :return: channel used to publish message
    """
    if chan is None or chan.is_closed:
        chan = initialize_rabbit_channel()

    chan.basic_publish(exchange=exchange_name, routing_key=routing_key, body=body)

    return chan
