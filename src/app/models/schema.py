class SchemaModel:
    def self_dump(self):
        return self.schema().dump(self)

    @classmethod
    def load(cls, **kattrs):
        return cls.schema().load(**kattrs)

    @classmethod
    def dump(cls, _id: int):
        return cls.schema().dump(cls.get(_id))

    @classmethod
    def dump_all(cls):
        return [_cls.self_dump() for _cls in cls.get_all()]
