import json
from urllib.parse import quote_plus

from pymongo import mongo_client


# import configs


class MongoCache:
    def __init__(
        self,
        username,
        password,
        client=None,
        disk_cache=None,
        host="localhost",
        db_name="video_cache",
        collection_name="default",
    ):

        uri = "mongodb://%s:%s@%s" % (quote_plus(username), quote_plus(password), host)
        self.client = mongo_client.MongoClient(uri) if not client else client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.disk_cache = disk_cache

    def __getitem__(self, key):
        # if db_name:
        record = self.collection.find_one({"_id": key})
        if record:
            return record["key"]
        elif self.disk_cache and self.disk_cache[key]:
            self[key] = self.disk_cache[key]
            return self.disk_cache[key]
        else:
            raise KeyError("{} cache does not exist".format(key))

    def __setitem__(self, key, value):
        self.collection.update_one({"_id": key}, {"$set": {"key": value}}, upsert=True)

    def length(self, collection=None):
        if collection:
            return self.db[collection].count()
        return self.collection.count()

    def items(self, collection=None):
        if collection:
            collection = self.db[collection]
        else:
            collection = self.collection
        res = collection.find()
        for r in res:
            yield r

    def keys(self, collection=None):
        if collection:
            collection = self.db[collection]
        else:
            collection = self.collection
        res = collection.find()
        for r in res:
            yield r["_id"]

    def values(self, collection=None):
        if collection:
            collection = self.db[collection]
        else:
            collection = self.collection
        res = collection.find()
        for r in res:
            try:
                yield json.loads(r["key"])
            except json.JSONDecodeError:
                yield r["key"]

    def change_collection(self, collection_name):
        if not collection_name:
            return
        self.collection = self.db[collection_name]

    def set(self, collection_name, key, value):
        self.db[collection_name].update_one(
            {"_id": key}, {"$set": {"key": value}}, upsert=True
        )

    def get(self, collection_name, key):
        record = self.db[collection_name].find_one({"_id": key})
        if not record:
            raise KeyError("{} cache does not exist".format(key))
        return record[key]


# if __name__ == "__main__":
#     a = MongoCache(db_name="video")
#     a.items()
# a.set(key='names', value='fjl3', collection="test_cache", db_name='video')
