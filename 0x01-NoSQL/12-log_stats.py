#!/usr/bin/env python3
"""  Log stats """

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    total = logs.count_documents({})
    print(f"{total} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = logs.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    filter_path = {"method": "GET", "path": "/status"}
    count = logs.count_documents(filter_path)
    print(f"{count} status check")
    client.close()
