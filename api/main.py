import os
from fastapi import FastAPI
from peewee import *
from pydantic import BaseModel
from datetime import date

db = PostgresqlDatabase(os.environ["POSTGRES_DATABASE"],
                           user=os.environ["POSTGRES_USER"],
                           password=os.environ["POSTGRES_PASSWORD"],
                           host=os.environ["POSTGRES_HOST"],
                           port=5432)

db.connect()

class User(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db

app = FastAPI()

@app.get("/")
def get_root():
    return "!"

@app.get("/db_test")
def db_test():
    db.create_tables([User])
    u1 = User(name='Bob', birthday=date(1960, 1, 15))
    u1.save()

    return "!"