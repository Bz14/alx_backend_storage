#!/usr/bin/env python3
"""Web module"""

import requests
import redis
from typing import Callable
import functools

r = redis.Redis()


def data_cache(method: Callable) -> Callable:
    """Decorator that stores the return value of a method"""
    @functools.wraps(method)
    def wrapper(*args, **kwargs) -> str:
        key = f"count:{args}"
        r.incr(key)
        value = r.get(key)
        if value:
            return value.decode('utf-8')
        value = method(*args, **kwargs)
        r.set(key, 0)
        r.setx(key, 10, value)
        return value
    return wrapper



@data_cache
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and returns it"""
    return requests.get(url).text