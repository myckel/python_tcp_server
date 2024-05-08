import asyncio
from asyncio import AbstractEventLoop, Future
import logging

# Set up logging
logger = logging.getLogger(__name__)

class SessionTracker:
    """
    Tracks and manages active sessions for an asynchronous TCP server.
    """

    def __init__(self, loop: AbstractEventLoop = None):
        self.sessions = set()
        self.loop = loop or asyncio.get_event_loop()

    def add_session(self, session):
        """
        Adds a new session to the tracker.

        Parameters:
            session: The session object to add to the tracker.
        """
        if session not in self.sessions:
            self.sessions.add(session)
            logger.info(f"Session added: {session}")
            session.add_done_callback(self.remove_session)

    def remove_session(self, session_future: Future):
        """
        Removes a session from the tracker when it is completed or cancelled.

        Parameters:
            session_future: The future object representing the session.
        """
        session = session_future.get_loop()
        if session in self.sessions:
            self.sessions.remove(session)
            logger.info(f"Session removed: {session}")

    def get_active_sessions(self):
        """
        Returns a set of all active sessions.

        Returns:
            A set of active session objects.
        """
        return self.sessions

    def session_count(self):
        """
        Returns the number of active sessions.

        Returns:
            Integer count of active sessions.
        """
        return len(self.sessions)


