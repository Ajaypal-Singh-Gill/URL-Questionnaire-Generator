import redis
import hashlib
import json
import os
# Initialize Redis connection
redis_client = redis.from_url(os.getenv('REDIS_URL'), decode_responses=True)


def hash_url(url):
    return url
    """Generate a unique hash for a given URL."""
    return hashlib.sha256(url.encode('utf-8')).hexdigest()


def get_cached_data(url):
    """Retrieve cached data from Redis."""
    url_hash = hash_url(url)
    cached_data = redis_client.get(url_hash)
    if cached_data:
        return json.loads(cached_data)
    return None


def set_cache_data(url, data, expiry=3600):
    """Store data in Redis with an expiration time."""
    url_hash = hash_url(url)
    redis_client.set(url_hash, json.dumps(data), ex=expiry)


def delete_cache_data(url):
    """Delete cached data from Redis."""
    url_hash = hash_url(url)
    redis_client.delete(url_hash)
