import json
from datetime import datetime

from peewee import *
from playhouse.sqlite_ext import JSONField

# SQLite database
db = SqliteDatabase("ita.db")

# Define a custom JSON property for the model
def json_property(attr_name, default=None):
    def getter(self):
        raw = getattr(self, attr_name)
        if raw is None:
            return default() if callable(default) else default
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return default() if callable(default) else default

    def setter(self, value):
        setattr(self, attr_name, json.dumps(value))

    return property(getter, setter)

def add_json(column):
    field = TextField(column_name=column, null=True)
    prop = json_property(f"_{column}")
    return prop, field

class BaseModel(Model):
    id = PrimaryKeyField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db
        legacy_table_names = False

    def pre_save(self, created):
        if not created:
            self.updated_at = datetime.now()
        return super().pre_save(created)

class Experiment(BaseModel):
    name = CharField()
    header, _header = add_json("header")

    @property
    def data(self):
        return [d for d in Data.select().where(Data.experiment == self.id)]

class Device(BaseModel):
    name = CharField(default="")
    hash = CharField(unique=True)

class Data(BaseModel):
    experiment = ForeignKeyField(Experiment, backref='data')
    device = ForeignKeyField(Device, backref='data')

    t0 = BigIntegerField()
    t1 = BigIntegerField()
    cols, _cols = add_json("cols")

db.connect()
db.create_tables([Data, Experiment, Device], safe=True)
