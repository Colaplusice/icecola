# utils for Flask Web & Crawler

[![image](https://travis-ci.org/Colaplusice/icecola.svg?branch=master)](https://travis-ci.org/Colaplusice/icecola)


#### philosophy: DRY don't repeat yourself

## install

pip3 install icecola

## flask_utils

- ModelViewSet: quickly build CRUD for REST api, like django_restframework

views.py
```python
from flask_utils.restframework import ModelViewSet

from jasmine_app.models.user import User
from jasmine_app.models.video import Video


class UserView(ModelViewSet):
    model_class = User


class Video(ModelViewSet):
    model_class = Video

```

urls.py
```python
from jasmine_app.api.views import UserView, Video
from flask_utils.views import register_api

from . import api

register_api(api, Video, "video_api", "/video/")
register_api(api, UserView, "user_api", "/user/")

```

## crawler utils

add cache implement for crawler

```python
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

```