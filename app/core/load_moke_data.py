import json
from ..db.redis_client import redis_client
VALID_USERS_SET = "valid_users"


def load_users_to_redis():
    with open("data/valid_user.json", "r") as file:
        data = json.load(file)

    for user_id in data.get("valid_users", []):
        redis_client.sadd(VALID_USERS_SET, user_id)
    print("Valid users loaded into Redis successfully!")