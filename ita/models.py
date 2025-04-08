import json
from datetime import datetime
from peewee import *
from playhouse.signals import Model, pre_save

from playhouse.sqlite_ext import JSONField

# SQLite database
db = SqliteDatabase("ita.db")

# Define a custom JSON property for the model
def json_property(field_name, default={}):
    def getter(self):
        raw = getattr(self, field_name)
        if raw is None:
            return default() if callable(default) else default
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return default() if callable(default) else default

    def setter(self, value):
        if isinstance(value, dict):
            raw = json.dumps(value)
        elif isinstance(value, str):
            raw = value
        else:
            raise ValueError("Must be dict or JSON string")
        setattr(self, field_name, raw)

    return property(getter, setter)

class BaseModel(Model):
    id = PrimaryKeyField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db
        legacy_table_names = False

    @pre_save()
    def update_timestamp(sender, instance, created):
        if hasattr(instance, 'updated_at'):
            if not created:
                instance.updated_at = datetime.now()

class Setting(BaseModel):
    name = CharField(default="")
    _config = TextField(column_name='config', null=True)
    config = json_property('_config')

class Experiment(BaseModel):
    setting = ForeignKeyField(Setting, backref='experiments')
    name = CharField()
    _header = TextField(column_name='header', null=True)
    header = json_property('_header')

    @property
    def data(self):
        return [d for d in Data.select().where(Data.experiment == self.id)]

class Device(BaseModel):
    name = CharField(default="")
    hash = CharField(unique=True)

class Data(BaseModel):
    experiment = ForeignKeyField(Experiment, backref='data')
    device = ForeignKeyField(Device, backref='data')
    updated_at = None

    t0 = BigIntegerField()
    t1 = BigIntegerField()
    _cols = TextField(column_name='cols', null=True)
    cols = json_property('_cols')

db.connect()
db.create_tables([Data, Experiment, Device, Setting], safe=True)
