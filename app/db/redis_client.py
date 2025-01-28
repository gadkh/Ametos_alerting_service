from dotenv import load_dotenv
import os
import redis

running_in_docker = os.getenv("RUNNING_IN_DOCKER")
if not running_in_docker:
    load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
# REDIS_HOST = "alerting_redis"
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
