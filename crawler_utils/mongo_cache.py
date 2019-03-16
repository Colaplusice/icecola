import json
from urllib.parse import quote_plus

from pymongo import mongo_client


# import configs


class MongoCache:
    def __init__(
        self,
        db_name,
        collection_name,
        username=None,
        password=None,
        client=None,
        host="localhost",
    ):
        """
        Cache based on Mongodb to save crawler messages
        a = MongoCache(db_name="video")
        a.items()
        a.set(key='names', value='fjl3', collection="test_cache", db_name='video')
        a[key]=value
        :param username: mongodb username
        :param password: mongodb password
        :param client:  client to connect mongodb
        :param disk_cache:  cache for disk if not exist in mongodb then will look in disk_cache
        :param host: mongodb server host
        :param db_name: database name
        :param collection_name:  collection name
        """
        if not username or not password:
            client = mongo_client.MongoClient()
        else:
            uri = "mongodb://%s:%s@%s" % (
                quote_plus(username),
                quote_plus(password),
                host,
            )
            client = mongo_client.MongoClient(uri) if not client else client
        self.db = client[db_name]
        self.collection = self.db[collection_name]

    def __getitem__(self, key):
        # if db_name:
        return self.get(self.collection.name, key)

    def __setitem__(self, key, value):
        self.set(self.collection.name, key, value)

    def __len__(self):
        return self.length(self.collection.name)

    def length(self, collection):
        """
        return collection all counts
        :param collection:
        :return:
        """
        return self.db[collection].estimated_document_count()

    def items(self, collection_name=None):
        """
        get all items from collection
        :param collection:
        :return: generator
        """
        if not collection_name:
            collection_name = self.collection.name
        collection = self.db[collection_name]
        res = collection.find()
        for r in res:
            yield r

    def keys(self, collection_name=None):
        """
        get all keys from collection
        :param collection:
        :return:
        """
        if not collection_name:
            collection_name = self.collection.name
        collection = self.db[collection_name]
        res = collection.find()
        for r in res:
            yield r["_id"]

    def values(self, collection_name=None):
        """
        get all values from collections
        :param collection:
        :return:
        """
        if not collection_name:
            collection_name = self.collection.name
        collection = self.db[collection_name]
        res = collection.find()
        for r in res:
            try:
                yield json.loads(r["key"])
            except json.JSONDecodeError:
                yield r["key"]

    def change_collection(self, collection_name):
        """
        change collection name
        :param collection_name:
        :return:
        """
        if not collection_name:
            return
        self.collection = self.db[collection_name]

    def set(self, collection_name, key, value):
        """
        set key for value
        :param collection_name:
        :param key:
        :param value:
        :return:
        """
        self.db[collection_name].update_one(
            {"_id": key}, {"$set": {"key": value}}, upsert=True
        )

    def get(self, collection_name, key):
        """
        get value from collection by key
        :param collection_name:
        :param key:
        :return:
        """
        record = self.db[collection_name].find_one({"_id": key})
        if not record:
            return None
        return record["key"]

    def __del__(self):
        self.destroy(self.collection.name)

    def destroy(self, collection_name=None, filter={}, **kwargs):
        if not collection_name:
            collection_name = self.collection.name
        self.db[collection_name].delete_many(filter, **kwargs)
