def test_mongo_cache(mongo_cache):
    key1 = "key"
    value1 = "value"

    mongo_cache[key1] = value1
    assert mongo_cache[key1] == value1
    assert len(mongo_cache) == 1
    assert set(mongo_cache.keys()) == {key1}
    assert set(mongo_cache.values()) == {value1}
    mongo_cache[value1] = key1
    assert len(mongo_cache) == 2
    del mongo_cache[value1]
    assert not mongo_cache[value1]
    assert len(mongo_cache) == 1
    mongo_cache.destroy()
    assert len(mongo_cache) == 0
