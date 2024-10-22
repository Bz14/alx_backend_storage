#!/usr/bin/env python3
""" Insert a document in Python """

def list_all(mongo_collection):
    """ list all documents """
    if not mongo_collection:
        return []
    return mongo_collection.find()