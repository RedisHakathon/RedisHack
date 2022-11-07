 import os
INDEX_NAME = "index"
REDIS_HOST = os.environ.get("REDIS_HOST", "--host--name")
REDIS_PORT = os.environ.get("REDIS_PORT", --port--number)
REDIS_DB = os.environ.get("REDIS_DB", "--database_name--")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD","--password--")
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"