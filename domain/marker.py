import logging
import server.utils as utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Marker:
    class MarkerType:
        GUNSHOT = ("gun",)
        EXT_GUN = ("ext-1", "ext-2", "ext-gun")
        MARKER = ("mark",)
        LOCATION = ("loc",)
        UNKNOWN = ()

        @staticmethod
        def parse_protocol_string(proto_str):
            for marker_type, protocols in {
                Marker.MarkerType.GUNSHOT: "GUNSHOT",
                Marker.MarkerType.EXT_GUN: "EXT_GUN",
                Marker.MarkerType.MARKER: "MARKER",
                Marker.MarkerType.LOCATION: "LOCATION",
                Marker.MarkerType.UNKNOWN: "UNKNOWN"
            }.items():

                if proto_str in marker_type:
                    return protocols

            return "UNKNOWN"

    def __init__(self, time, label, location, type):
        self.time = time
        self.label = label
        self.location = location
        self.type = type

    @staticmethod
    def parse_marker(part, location="Unknown Location"):
        try:
            details = part.split('|')
            if len(details) != 3:
                logger.warning(f"Invalid format for marker data: {part}")

                return None

            time_str, tag, description = details
            time_milliseconds = utils.parse_date_time_string(time_str)

            if time_milliseconds is None:
                return None  # Early exit if time parsing fails

            marker_type = Marker.MarkerType.parse_protocol_string(tag)

            return Marker(time_milliseconds, description, location, marker_type)
        except Exception as e:
            logger.error(f"Failed to parse marker: {part}. Error: {e}")

            return None

    @staticmethod
    def parse_markers(message):
        message_parts = message.split('@')

        if len(message_parts) < 3:
            logger.error(f"Message format incorrect, missing parts {message_parts}")

            return []

        location = message_parts[0]
        parts = [part for part in message_parts if '|' in part]
        markers = []

        for part in parts:
            marker = Marker.parse_marker(part, location)

            if marker:
                markers.append(marker)

        return markers

    def __str__(self):
        return f"Marker(time={self.time}, label='{self.label}', location='{self.location}', type='{self.type}')"
