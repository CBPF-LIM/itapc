import json
from datetime import datetime

from peewee import *
from playhouse.sqlite_ext import JSONField

# SQLite database
db = SqliteDatabase("ita.db")

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
    _header = TextField(column_name="header", default="[]")

    @property
    def header(self):
        return json.loads(self._header)

    @header.setter
    def header(self, value):
        self._header = json.dumps(value)

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
    _cols = TextField(column_name="cols")

    @property
    def cols(self):
        return json.loads(self._cols)

    @cols.setter
    def cols(self, value):
        self._cols = json.dumps(value)

db.connect()
db.create_tables([Data, Experiment, Device], safe=True)
