#!/usr/bin/python3
"""initializes package"""
from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
