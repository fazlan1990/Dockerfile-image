from flask import jsonify
import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

def store_data(key, value):
    try:
        redis_client.set(key, value)
    except Exception as e:
        print(f"Error storing data: {e}")

def retrieve_data(key):
    try:
        result = redis_client.get(key)
        if result:
            return result.decode("utf-8")
        else:
            return None
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None

def insert_records(username, team_domain, sdesk_url, sdesk_api_key):
    str_list=[username, team_domain]
    id = "@".join(str_list)
    redis_client.hmset(f"Users:{id}", {
        "username": username,
        "team_domain": team_domain,
        "sdesk_url": sdesk_url,
        "sdesk_api_key": sdesk_api_key
    })
    redis_client.sadd("Users:Ids", id)

    return "Records inserted successfully!"

def get_record(username, team_domain):
    str_list=[username, team_domain]
    id = "@".join(str_list)
    result = redis_client.hgetall(f"Users:{id}")
    if not result:
        return None
    record = {id: {key.decode("utf-8"): value.decode("utf-8") for key, value in result.items()}}

    user_data = record.get(id, {})

    sdesk_url = user_data.get("sdesk_url")
    sdesk_api_key = user_data.get("sdesk_api_key")

    return sdesk_url, sdesk_api_key
