#!/usr/bin/env python3
"""Exercise"""


import redis
from typing import Union


class Cache:
    """A cache class """
    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
