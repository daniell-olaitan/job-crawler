#!/usr/bin/env python3
"""
Module that create a db instance
"""
from models.engines.mongodb_storage import MongoDBStorage

db = MongoDBStorage()
