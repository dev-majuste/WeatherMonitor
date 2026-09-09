import threading
import time


class RateLimitService:
    _requests = {}
    _lock = threading.Lock()

    @classmethod
    def check(cls, api_key: str, limit: int):
        now = time.time()

        with cls._lock:
            data = cls._requests.get(api_key)

            if data is None or now - data["start"] >= 60:
                cls._requests[api_key] = {
                    "start": now,
                    "count": 1
                }

                return True

            if data["count"] >= limit:
                return False

            data["count"] += 1

            return True