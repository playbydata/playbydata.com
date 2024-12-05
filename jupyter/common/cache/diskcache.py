from diskcache.core import Cache as DiskCache, full_name, ft, ENOVAL

import settings


__all__ = ("disk_cache",)


class Cache(DiskCache):
    def memoize(self, name=None, typed=False, expire=None, tag=None, ignore=()):
        def decorator(func):
            """Decorator created by memoize() for callable `func`."""
            @ft.wraps(func)
            def wrapper(*args, **kwargs):
                """Wrapper for callable to cache arguments and return values."""
                if callable(name):
                    key = name(*args, **kwargs)
                elif name:
                    key = str(name)
                else:
                    key = f"{full_name(func)}.{".".join(map(str, args))}.{kwargs}"

                result = self.get(key, default=ENOVAL, retry=True)

                if result is ENOVAL or settings.RESET_CACHE:
                    result = func(*args, **kwargs)
                    if expire is None or expire > 0:
                        self.set(key, result, expire, tag=tag, retry=True)

                return result
            return wrapper
        return decorator


disk_cache = Cache(directory=settings.LOCAL_STORAGE_PATH, size_limit=10 * 1024 * 1024 * 1024)
