from functools import wraps
import copy


def memoize(func):
    _cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        try:
            return copy.copy(_cache[key])
        except TypeError:  # Unhashable key
            return func(*args, **kwargs)
        except KeyError:
            value = func(*args, **kwargs)
            _cache[key] = value
            return copy.copy(value)

    return wrapper
