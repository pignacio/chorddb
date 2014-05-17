from functools import wraps


def memoize(func):
    _cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        try:
            return _cache[key]
        except TypeError:  # Unhashable key
            return func(*args, **kwargs)
        except KeyError:
            value = func(*args, **kwargs)
            _cache[key] = value
            return value

    return wrapper
