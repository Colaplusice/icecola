from peewee import DoesNotExist, IntegrityError


class SerializerMixin:
    @classmethod
    def update_or_create(cls, **kwargs):
        defaults = kwargs.pop("defaults")
        query = cls.select()
        for field, value in kwargs.items():
            query = query.where(getattr(cls, field) == value)
        try:
            instance = cls.get()
            instance.update(**kwargs).execute()
            return instance, False
        except DoesNotExist:
            try:
                if defaults:
                    kwargs.update(defaults)
                    with cls._meta.database.atomic:
                        return cls.create(**kwargs), True
            except IntegrityError as exc:
                try:
                    return query.get(), False
                except DoesNotExist:
                    raise exc
