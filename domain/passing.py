import logging
from typing import List
import server.utils as utils

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class Passing:
    def __init__(self, time: int, chip_code: str, location: str):
        self.time = time
        self.chip_code = chip_code
        self.location = location

    @staticmethod
    def parse_times(message: str) -> List['Passing']:
        passings = []
        message_parts = message.split('@')
        location = message_parts[0]

        # Start parsing from the third part and avoid the last two parts which are not needed
        parts = message_parts[2:-2]  # This will ignore the last parts like '3@$'
        for part in parts:
            # Splitting each part into details based on spaces
            details = part.split()
            chip_time_combo = details[0]
            chip_code = chip_time_combo[:7]
            time_str = chip_time_combo[7:]
            time = utils.parse_date_time_string(time_str)

            if len(chip_code) == 7 and time is not None:
                passing = Passing(time, chip_code, location)
                passings.append(passing)

        return passings

    def __repr__(self):
        return f"<Passing time={self.time}, chip_code='{self.chip_code}', location='{self.location}'>"
