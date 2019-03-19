from faker import Factory
import peewee
import random
import datetime
from urllib.parse import urljoin
from functools import wraps
import pytest
from playhouse.shortcuts import model_to_dict

faker = Factory.create()


def fake_fixture_drop(entities):
    for name, entity in entities.items():
        entity.delete()


def fake_data(model, **kwargs):
    def get_value(c, *args, **kwargs):
        if callable(c):
            return c(*args, **kwargs)
        else:
            return c

    field_name_map = kwargs.get("field_name_map", {})
    custom_field_type_map = kwargs.get("custom_field_type_map", {})
    skip_id = kwargs.get("skip_id", False)

    field_type_map = {
        peewee.DateTimeField: datetime.datetime.now,
        peewee.CharField: faker.word,
        peewee.IntegerField: random.randrange(1, 32767),
        peewee.BooleanField: random.choice([True, False]),
        peewee.AutoField: random.randint(1, 1000),
        peewee.SmallIntegerField: random.randint(1, 128),
    }
    model_data = {}
    field_type_map.update(custom_field_type_map)
    for field_name, field_type in model._meta.fields.items():
        if skip_id and field_name == "id":
            continue
        else:
            if field_name in field_name_map:
                field_value = get_value(field_name_map[field_name])
            elif type(field_type) in field_type_map:
                field_value = get_value(field_type_map[type(field_type)])
            elif type(field_type) is peewee.ForeignKeyField:
                field_value = field_type.rel_model.select().first()
            elif hasattr(faker, field_name):
                field_value = getattr(faker, field_name)()
            else:
                raise NotImplementedError
            model_data[field_name] = field_value
    return model_data


def fake_fixture(model, on_failure=None, **kwargs):
    model_data = fake_data(model, **kwargs)
    try:
        nm = model.create(**model_data)
        return nm
    except Exception as ex:
        if on_failure:
            on_failure(ex.args, model_data)


def fake_api(Model, url_prefix="/api/", url_path=None, exclude_methods=()):
    def decorate(func):
        @wraps(func)
        def wrapper(client):
            if client is None:
                return
            _url_path = url_path
            if _url_path is None:
                _url_path = Model._meta.name
            url = urljoin(url_prefix, _url_path + "/")
            model_data = fake_data(Model)
            # post
            if "POST" not in exclude_methods:
                res = client.post(url, json=model_data)
                assert res.status_code == 201
                model_data = fake_data(Model)
                res = client.post(url, json=model_data)
                assert res.status_code == 201
            # list
            if "LIST" not in exclude_methods:
                res = client.get(url)
                assert res.status_code == 200
                assert len(res.json) == 2
            # get
            if "GET" not in exclude_methods:
                res = client.get(urljoin(url, str(model_data["id"])))
                assert res.status_code == 200
                assert res.json == model_data
            # put
            if "PUT" not in exclude_methods:
                update_data = fake_data(Model, field_name_map={"id": model_data["id"]})
                res = client.put(urljoin(url, str(update_data["id"])), json=update_data)
                assert res.status_code == 204
                model_data = model_to_dict(
                    Model.get_by_id(update_data["id"]), recurse=False
                )
                assert update_data == model_data
            # delete
            if "DELETE" not in exclude_methods:
                delete_model_id = model_data["id"]
                res = client.delete(urljoin(url, str(delete_model_id)))
                assert res.status_code == 204
                with pytest.raises(peewee.DoesNotExist):
                    Model.get_by_id(delete_model_id)

        return wrapper

    return decorate
