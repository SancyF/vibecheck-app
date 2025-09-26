import time
import json

class SimpleCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key, max_age=300):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < max_age:
                return data
        return None
    
    def set(self, key, value):
        self.cache[key] = (value, time.time())
    
    def clear(self):
        self.cache.clear()

# Global cache instance
cache = SimpleCache()