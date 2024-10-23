#!/usr/bin/env python3
"""Exercise"""


import functools
import redis
from typing import Union
from typing import Callable

def call_history(method: Callable) -> Callable:
    """Decorator to store history of inputs and outputs for a function"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.rpush(key + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(key + ":outputs", output)
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls to a method using Redis"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """A cache class """
    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis"""
        import uuid
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: callable = None):
        """Get data from Redis"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Get a string from Redis"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Get an int from Redis"""
        return self.get(key, int)
