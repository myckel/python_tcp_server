import logging
from domain.passing import Passing
from domain.marker import Marker
from server.data_handler import ServerDataHandler
from typing import Collection

# Set up logging
logger = logging.getLogger(__name__)

class SampleServerHandler(ServerDataHandler):
    def __init__(self):
        # Initialize any necessary attributes or services here
        self.server_name = "SampleServer"
        self.server_port = 3097

    def handle_passings(self, passings: Collection[Passing]):
        """
        Processes each passing object received.
        """
        for passing in passings:
            logger.info(f"Processed Passing: chip {passing.chip_code} at {passing.location}, time: {passing.time}")

    def handle_markers(self, markers: Collection[Marker]):
        """
        Processes each marker object received.
        """
        for marker in markers:
            logger.info(f"Processed Marker: {marker.label} at {marker.location} of type {marker.type}, time: {marker.time}")

    def handle_login(self, username: str, password: str) -> bool:
        """
        Simulates user authentication.
        Assumes all logins are successful for demonstration purposes.
        """
        logger.info(f"Login attempt by {username}")
        # In a real application, you would check credentials against a database or other secure storage
        return True

    def get_server_name(self) -> str:
        """
        Returns the server name.
        """
        return self.server_name

    def get_server_port(self) -> int:
        """
        Returns the server port number.
        """
        return self.server_port
