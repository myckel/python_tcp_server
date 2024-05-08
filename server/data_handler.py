from abc import ABC, abstractmethod
from domain.passing import Passing
from domain.marker import Marker
from typing import Collection
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ServerDataHandler(ABC):
    """
    Abstract base class for server data handlers. Defines the template methods that
    all subclasses need to implement for handling different types of data.
    """

    @abstractmethod
    def handle_passings(self, passings: Collection[Passing]):
        """
        Handle the collection of Passing objects.

        Parameters:
            passings (Collection[Passing]): A collection of Passing objects.
        """
        pass

    @abstractmethod
    def handle_markers(self, markers: Collection[Marker]):
        """
        Handle the collection of Marker objects.

        Parameters:
            markers (Collection[Marker]): A collection of Marker objects.
        """
        pass

    @abstractmethod
    def handle_login(self, username: str, password: str) -> bool:
        """
        Handle login requests. Return True if credentials are accepted, False otherwise.

        Parameters:
            username (str): The user's username.
            password (str): The user's password.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_server_name(self) -> str:
        """
        Returns the server name.

        Returns:
            str: The name of the server.
        """
        pass

    @abstractmethod
    def get_server_port(self) -> int:
        """
        Returns the server port number.

        Returns:
            int: The port number on which the server is running.
        """
        pass

