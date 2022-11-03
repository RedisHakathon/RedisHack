import os

INDEX_NAME = "index"
REDIS_HOST = os.environ.get("REDIS_HOST", "redis-16644.c282.east-us-mz.azure.cloud.redislabs.com")
REDIS_PORT = os.environ.get("REDIS_PORT", 16644)
REDIS_DB = os.environ.get("REDIS_DB", "arvix-dataset")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD","ICe9oFTnhXr3s8oVz8CB1ljNu7jHZQiH")
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

