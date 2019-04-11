import pytest

from icecola.crawler_utils import MongoCache


@pytest.fixture
def mongo_cache():
    cache = MongoCache(db_name="test", collection_name="default")
    cache.destroy()
    yield cache
    cache.destroy()
