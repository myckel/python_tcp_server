import asyncio
import logging
import settings
from server.tcp_server import TCPProtocol
from server.sample_handler import SampleServerHandler
from config import clear_redis_database

# Setting up logging
settings.setup_logging()
logger = logging.getLogger(__name__)

async def start_server():
    # Clear Redis database
    clear_redis_database()

    # Initialize the data handler
    handler = SampleServerHandler()

    # Retrieve server configurations
    server_name = handler.get_server_name()
    server_port = handler.get_server_port()

    # Setup the TCP server
    loop = asyncio.get_running_loop()
    server = await loop.create_server(
        lambda: TCPProtocol(handler),
        '0.0.0.0',  # Bind to all interfaces
        server_port
    )

    logger.info(f'{server_name} is listening on {server_port}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(start_server())
    except Exception as e:
        logger.error('An error occurred while starting the server', exc_info=True)
