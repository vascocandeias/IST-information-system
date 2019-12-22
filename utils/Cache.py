import time

class Cache:
    def __init__(self, size, days=0, hours=0, minutes=0, seconds=0):
        self.size = size
        self.ttl = days*24*60*60 + hours*60*60 + minutes*60 + seconds
        self.cache = {}
    
    def put(self, key, content):
        obj = {
            key: {
                "content": content,
                "start": time.time(),
            }
        }

        if len(self.cache) >= self.size:
            self.cache.pop(next(iter(self.cache)))
        
        try:
            self.cache.pop(key)
        except:
            pass

        self.cache.update(obj)

    def get(self, key):
        obj = self.cache.get(key)

        if obj is None:
            return None
        if time.time() - obj["start"] >= self.ttl:
            self.cache.pop(key)
            return None

        return obj["content"]
        