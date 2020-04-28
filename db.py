from collections import defaultdict
import pickle


class DB():
    def __init__(self, db_file):
        self._db_file = db_file
        try:
            with open(self._db_file, 'rb') as f:
                self.kv = pickle.load(f)
        except FileNotFoundError:
            self.kv = defaultdict(dict)

    def get(self, bucket, key):
        return self.kv[bucket][key]

    def put(self, bucket, key, val):
        self.kv[bucket][key] = val

    def delete(self, bucket, key):
        del self.kv[bucket][key]

    def save(self):
        with open(self._db_file, 'wb') as f:
            pickle.dump(self.kv, f)

    def reset(self, bucket):
        self.kv[bucket] = {}


class Bucket():

    def __init__(self, db_file, bucket):
        self._db = DB(db_file)
        self._bucket = bucket

    def reset(self):
        self._db.reset(self._bucket)

    def get(self, key):
        return self._db.get(self._bucket, key)

    def put(self, key, value):
        self._db.put(self._bucket, key, value)

    def delete(self, key):
        self._db.delete(self._bucket, key)

    def save(self):
        self._db.save()

    @property
    def kv(self):
        return self._db.kv[self._bucket]
