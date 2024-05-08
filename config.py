from dotenv import load_dotenv
import os
import redis
import logging
import settings


# Setting up logging
settings.setup_logging()
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get Redis credentials from environment variables
redis_host = os.getenv("REDIS_HOST", 'localhost')
redis_port = os.getenv("REDIS_PORT", 6379)
redis_username = os.getenv("REDIS_USERNAME", "")
redis_password = os.getenv("REDIS_PASSWORD", "")

# Establish a connection to Redis
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    username=redis_username,
    password=redis_password,
    decode_responses=True
)

def clear_redis_database():
    """Clears all keys from the current Redis database."""
    try:
        redis_client.flushdb()
    except Exception as e:
        logger.error(f"Failed to clear Redis database: {e}")
