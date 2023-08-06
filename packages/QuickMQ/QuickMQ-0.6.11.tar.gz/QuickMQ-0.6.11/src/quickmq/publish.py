from contextlib import contextmanager
import threading
from typing import Generator, Optional
import logging

from quickmq.connection import ConnectionPool, ServerConnection

from .message import Packet

# Possible problem with lock when publishing to multiple servers
# When one server is reconnecting, publishing will pause for all connections!

LOGGER = logging.getLogger(__name__)


class AmqpPublisher:
    def __init__(self) -> None:
        self._publishing = threading.Event()
        self._publishing.set()  # not publishing, don't want threads to block
        self._publishing_err: Optional[Exception] = None

    @contextmanager
    def sync_connection(
        self, to_raise: Optional[Exception] = None
    ) -> Generator[None, None, None]:
        self._publishing.clear()
        yield
        LOGGER.debug("Waiting for connection thread to finish publishing")
        self._publishing.wait()
        if self._publishing_err is None:
            return
        LOGGER.warning(f"Error detected while publishing: {self._publishing_err}")
        err = to_raise or self._publishing_err
        self._publishing_err = None
        raise err

    def _publish(self, connection: ServerConnection, packet: Packet) -> None:
        try:
            pub_channel = (
                connection._confirmed_channel if packet.confirm else connection._channel
            )
            with connection.prepare_connection():
                LOGGER.info(
                    f"Connection prepared, attempting to publish to {packet.exchange} exchange on {connection.server}"
                )
                pub_channel.basic_publish(
                    packet.exchange,
                    routing_key=packet.routing_key,
                    body=bytes(packet.message.encode(), "utf-8"),
                    properties=packet.properties,
                )
                LOGGER.info(f"Published {packet} to {connection.server}")
        except Exception as e:
            self._publishing_err = e
            LOGGER.warning(f"Couldn't publish to exchange {packet.exchange} on {connection.server} because {e}")
        finally:
            self._publishing.set()

    def publish_to_connection(self, connection: ServerConnection, pckt: Packet) -> None:
        if not pckt.confirm:
            return connection.add_callback(self._publish, connection, pckt)
        with self.sync_connection():
            connection.add_callback(self._publish, connection, pckt)

    def publish_to_pool(
        self, pool: ConnectionPool, pckt: Packet
    ) -> None:
        for con in pool:
            self.publish_to_connection(con, pckt)
