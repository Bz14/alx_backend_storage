#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient


def log_stats():
    """ Log stats """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    log_count = nginx_collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts[method] = nginx_collection.count_documents(
            {"method": method})

    status_check_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})

    # Display results
    print(f"{log_count} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()
