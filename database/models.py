from peewee import (SqliteDatabase, Model, IntegerField, CharField, TextField,
                    ForeignKeyField)

db = SqliteDatabase('TelebotDatabase.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(unique=True)
    chat_id = IntegerField(unique=True)

    class Meta:
        db_table = 'Users'


class Character(BaseModel):
    owner = ForeignKeyField(User, backref='character')
    name = CharField(max_length=15)
    char_class = CharField(max_length=15)
    race = CharField(max_length=15)
    balance = IntegerField(default=0)
    level = IntegerField(default=1)
    equipment = TextField(default='')

    class Meta:
        db_table = 'Characters'


def initialize_db():
    db.connect()
    db.create_tables([Character, User])
