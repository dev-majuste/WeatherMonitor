import threading


class CacheService:
    _cache = {}
    _lock = threading.Lock()

    @classmethod
    def get(cls, key: str):
        with cls._lock:
            return cls._cache.get(key)

    @classmethod
    def set(cls, key: str, value):
        with cls._lock:
            cls._cache[key] = value

    @classmethod
    def clear(cls):
        with cls._lock:
            cls._cache.clear()