import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def part_to_map(part: str):
    parts_map = {}
    passing_parts = part.split("|")

    for passing_part in passing_parts:
        kv = passing_part.split("=")

        if len(kv) != 2:
            logger.warn(f"Invalid key-value pair: {part}")
            continue
        parts_map[kv[0]] = kv[1]

    return parts_map

def parse_date_time_string(date_time_str):
    """
    Parse a datetime string to a datetime object converted to UTC and return milliseconds since the epoch.
    """
    formats = ["%Y-%m-%d %H:%M:%S.%f", "%H:%M:%S.%f"]  # List of date formats to try

    for fmt in formats:
        try:
            # Check if the format requires prepending today's date
            if fmt == "%H:%M:%S.%f":
                current_date_str = datetime.now().strftime("%Y-%m-%d ")
                temp_date_time_str = current_date_str + date_time_str
                dt = datetime.strptime(temp_date_time_str, "%Y-%m-%d %H:%M:%S.%f")
            else:
                dt = datetime.strptime(date_time_str, fmt)

            dt = dt.replace(tzinfo=timezone.utc)

            return int(dt.timestamp() * 1000)
        except ValueError:
            continue  # Try the next format if current one fails

    # Log an error if no formats matched
    logger.error(f"Error parsing date time string: {date_time_str}. No matching format found.")

    return None
