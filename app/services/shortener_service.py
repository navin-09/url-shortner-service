import hashlib, string
from app.repositories.url_repository import PostgresUrlRepository
from app.core.redis_client import redis_client
from app.core.config import settings
from sqlalchemy.orm import Session

# Base62 alphabet (a-zA-Z0-9)
BASE62_ALPHABET = string.ascii_letters + string.digits

def base62_encode(num: int) -> str:
    """Convert integer to base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    encoded = ""
    base = len(BASE62_ALPHABET)
    while num > 0:
        num, rem = divmod(num, base)
        encoded = BASE62_ALPHABET[rem] + encoded
    return encoded

class ShortCodeStrategy:
    """Strategy for deterministic short code generation."""
    def generate(self, url: str, length: int = 8) -> str:
        # hash_bytes = hashlib.sha256(url.encode()).digest()
        url_bytes = str(url).encode()
        hash_bytes = hashlib.sha256(url_bytes).digest()
        hash_int = int.from_bytes(hash_bytes, "big")
        code = base62_encode(hash_int)[:length]
        return code

class UrlService:
    """Business layer (follows Single Responsibility & Dependency Inversion)."""
    def __init__(self, repo: PostgresUrlRepository, base_url: str):
        self.repo = repo
        self.base_url = base_url
        self.strategy = ShortCodeStrategy()

    def create_short_url(self, db: Session, original_url: str):
        code = self.strategy.generate(original_url, settings.SHORT_CODE_LENGTH)
        mapping = self.repo.create_if_not_exists(db, code, original_url)
        short_url = f"{self.base_url}/{mapping.short_code}"
        # Cache short_code -> original_url for fast redirects
        redis_client.set(f"url:{mapping.short_code}", mapping.original_url, ex=60*60*24*7)  # 7 days
        return short_url, mapping.short_code

    def resolve_short_code(self, db: Session, code: str):
        # 1️⃣ Try Redis cache
        cached_url = redis_client.get(f"url:{code}")
        if cached_url:
            redis_client.incr(f"clicks:{code}")
            self.repo.increment_click(db, code)
            return cached_url

        # 2️⃣ Fallback to Postgres
        mapping = self.repo.get_by_code(db, code)
        if not mapping:
            return None

        # Cache and increment
        redis_client.set(f"url:{code}", mapping.original_url, ex=60*60*24*7)
        redis_client.incr(f"clicks:{code}")
        self.repo.increment_click(db, code)
        return mapping.original_url
