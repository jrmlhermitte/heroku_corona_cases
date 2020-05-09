import threading
import time


class CacheManager:
    def __init__(self):
        self._timestamps = {}
        self._cache = {}

    # https://stackoverflow.com/questions/21156519/python-cache-memorize-and
    # -thread-locking
    def memorize(self, key, period):
        """
        Memorizing decorator. Returning cached data
        if its validity period is not expired

        NOTE: If function raises, this won't set anything
            and the lock will be released.
        """
        # Access is locked for this key
        lock = threading.Lock()

        def _decoration_wrapper(func):
            def _caching_wrapper(*args, **kwargs):
                cache_key = key
                now = time.time()

                if self._timestamps.get(cache_key, now) > now:
                    return self._cache[cache_key]
                with lock:
                    if self._timestamps.get(cache_key, now) > now:
                        return self._cache[cache_key]
                    ret = func(*args, **kwargs)
                    self._cache[cache_key] = ret
                    self._timestamps[cache_key] = now + period
                    return ret

            return _caching_wrapper

        return _decoration_wrapper


cache_manager = CacheManager()
