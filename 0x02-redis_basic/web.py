#!/usr/bin/env python3
"""Web module"""

import redis
import requests
from functools import wraps
from typing import Callable


r = redis.Redis()


def data_cache(method: Callable) -> Callable:
    """Decorator that stores the return value of a method"""
    @wraps(method)
    def invoker(url) -> str:
        """ Invoker function """
        r.incr(f"count:{url}")
        value = r.get(f"count:{url}")
        if value:
            return value.decode('utf-8')
        value = method(url)
        r.set(f"count:{url}", 0)
        r.setx(f"count:{url}", 10, value)
        return value
    return invoker


@data_cache
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and returns it"""
    return requests.get(url).text
