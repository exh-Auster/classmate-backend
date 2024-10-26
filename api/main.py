import os
from fastapi import FastAPI
from pony.orm import *
from pydantic import BaseModel
from datetime import date

db = Database()

db.bind(provider='postgres',
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        database=os.environ["POSTGRES_DATABASE"])

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    email = Required(str, unique=True)
    password_hash = Optional(str) # TODO
    bio = Optional(str)
    registered_at = Optional(str) # TODO
    groups = Set('Group') # TODO
    posts = Set('Post') # TODO

class Group(db.Entity):
    id = PrimaryKey(int, auto=True)
    created_by = Required(User)
    name = Required(str, unique=True)
    description = Required(str)
    posts = Set('Post') # TODO
    
class Post(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(User)
    group = Required(Group)
    timestamp = Optional(str) # TODO
    text_content = Required(str)
    external_content_url = Optional(str) # TODO

app = FastAPI()

@app.get("/")
def get_root():
    return "!"

@app.get("/db_generate")
def db_test():
    db.generate_mapping(create_tables=True)

    return "!"

@app.get("/db_create")
def db_create():
    db.create_tables()

    return "!"

@app.get("/db_drop")
def db_drop():
    db.drop_all_tables(with_all_data=True)

    return "!"

@app.get("/db_add")
@db_session
def db_add():
    test = User(name="test", email="test")

    return test