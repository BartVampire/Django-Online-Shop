from django.test import TestCase
from django.core.cache import cache

try:
    cache.get("test_key")
except Exception as e:
    print(f"Error connecting to Redis: {e}")
else:
    print("Connected to Redis successfully!")
