#!/usr/bin/env python3
"""Web module"""

import requests
import redis

r = redis.Redis()


def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and returns it"""
    key = f"count:{url}"
    count = r.get(key)
    if count:
        r.incr(key)
        return r.get(url)
    else:
        r.set(key, 1)
        r.expire(key, 10)
        return requests.get(url).text
