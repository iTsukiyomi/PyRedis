import time, random

class DataStore:
    def __init__(self):
        self.data = {}
        self.expires = {}

    def _is_expired(self, key):
        if not key in self.expires:
            return False
        current = int(time.time() * 1000)

        if self.expires[key] <= current:
            del self.data[key]
            del self.expires[key]
            return True

        return False

    def set_expiry(self, key, ttl_ms):
        self._is_expired(key)
        if not key in self.data:
            return 0
        current_time_ms = int(time.time() * 1000)
        expiration = current_time_ms + ttl_ms

        self.expires[key] = expiration
        return 1

    def get_ttl_ms(self, key):
        self._is_expired(key)
        if key not in self.data:
            return -2
        if key not in self.expires:
            return -1
        return self.expires[key] - int(time.time() * 1000)

    def active_expiry_cycle(self):
        while True:
            keys = random.sample(
                        list(self.expires.keys()),
                        min(20, len(self.expires))
                    )

            expired_count = 0

            for key in keys:
                if self._is_expired(key):
                    expired_count +=1

            if expired_count <= 5:
                break

    def get(self, key):
        self._is_expired(key)
        return self.data.get(key, None)

    def set(self, key, value):
        self.data[key] = value
        self.expires.pop(key, None)

    def delete(self, *keys):
        deleted = 0
        for key in keys:
            if key in self.data:
                del self.data[key]
                self.expires.pop(key, None)
                deleted += 1
        return deleted

    def exists(self, *keys):
        count = 0
        for key in keys:
            self._is_expired(key)
            if key in self.data:
                count += 1
                
        return count

