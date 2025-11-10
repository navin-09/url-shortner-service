import redis
from app.core.config import settings

# Factory pattern — centralized creation
class RedisClientFactory:
    _client = None

    @classmethod
    def get_client(cls) -> redis.Redis:
        if cls._client is None:
            cls._client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        return cls._client

redis_client = RedisClientFactory.get_client()
