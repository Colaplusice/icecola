import pytest

from crawler_utils import MongoCache


@pytest.fixture
def mongo_cache():
    cache = MongoCache(db_name="test", collection_name="default")
    yield cache
    cache.destroy()
