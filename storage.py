

class DataStore:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key, None)

    def set(self, key, value):
        self.data[key] = value

    def delete(self, *keys):
        deleted = 0
        for key in keys:
            if key in self.data:
                del self.data[key]
                deleted += 1
        return deleted

    def exists(self, *keys):
        count = 0
        for key in keys:
            if key in self.data:
                count += 1
        return count

