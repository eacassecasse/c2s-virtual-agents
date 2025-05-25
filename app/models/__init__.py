#!/usr/bin/python3
"""
initialize the models package
"""

import os
from dotenv import load_dotenv

load_dotenv()

storage_t = os.getenv("C2S_TYPE_STORAGE")

if storage_t == "db":
    from app.storage.db_storage import DBStorage
    storage = DBStorage()
else:
    from app.storage.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
