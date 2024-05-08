import asyncio
import logging
from asyncio import StreamReader, StreamWriter
from server.data_handler import ServerDataHandler
from server.sample_handler import SampleServerHandler
from domain.marker import Marker
from domain.passing import Passing
from config import redis_client


logger = logging.getLogger(__name__)

class TCPProtocol(asyncio.Protocol):
    def __init__(self, handler: ServerDataHandler):
        self.handler = handler
        self.transport = None
        self.session = None
        self.session_id = None

    def create_unique_session_id(self):
        """Create a unique session ID using relevant attributes."""
        peer_name = self.transport.get_extra_info('peername')

        return f"{peer_name}-{id(self)}"

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        self.session = transport.get_extra_info('peername')
        self.session_id = self.create_unique_session_id()

    def data_received(self, data: bytes):
        message = data.decode('utf-8').strip()

        if 'Pong' in message:
            self.transport.write(data)
        else:
            self.process_data(message)

    def process_data(self, message):
        logger.info(f"Received RAW data from {self.session}: {message}")
        try:
            if 'Marker' in message:
                markers = Marker.parse_markers(message)
                unique_markers = [m for m in markers if self.add_if_not_processed_marker(m)]

                if unique_markers:
                    self.handler.handle_markers(unique_markers)
            elif 'Store' in message:
                passings = Passing.parse_times(message)
                unique_passings = [p for p in passings if self.add_if_not_processed_passing(p)]

                if unique_passings:
                    self.handler.handle_passings(unique_passings)
        except Exception as e:
            logger.error(f"Failed to process data from {self.session}: {str(e)}", exc_info=True)


    def add_if_not_processed_passing(self, passing):
        """Checks if the passing has been processed; returns True if not, and stores it."""
        passing_id = f"{passing.time}-{passing.chip_code}-{passing.location}"
        if not redis_client.exists(passing_id):
            redis_client.set(passing_id, "processed")

            return True

        return False

    def add_if_not_processed_marker(self, marker):
        """Adds the marker to the set if it hasn't been processed; returns True if added, False otherwise."""
        marker_id = f"{marker.time}-{marker.label}-{marker.type}"
        if not redis_client.exists(marker_id):
            redis_client.set(marker_id, "processed")

            return True

    def connection_lost(self, exc):
        logger.info(f"Connection lost with {self.session}: {exc}")
        if exc:
            logger.error(f"Error: {exc}")
        self.transport.close()

    def eof_received(self):
        return True

async def start_server(host: str, port: int, handler: ServerDataHandler):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(
        lambda: TCPProtocol(handler),
        host, port
    )

    async with server:
        await server.serve_forever()
