def test_mongo_cache(mongo_cache):
    key1 = "key"
    value1 = "value"

    mongo_cache[key1] = value1
    assert mongo_cache[key1] == value1
    assert len(mongo_cache) == 1
    assert set(mongo_cache.keys()) == {key1}
    assert set(mongo_cache.values()) == {value1}
    mongo_cache.destroy()
    assert len(mongo_cache) == 0



