import os

from datetime import date
from fastapi import FastAPI
from pony.orm import *

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
    following = Set('Connection', reverse='source')
    followers = Set('Connection', reverse='destination')
    groups = Set('Group') # TODO
    posts = Set('Post') # TODO
    comments = Set('Comment')
    likes = Set('Like')

class Connection(db.Entity): # TODO
    id = PrimaryKey(int, auto=True)
    source = Required(User, reverse='following')
    destination = Required(User, reverse='followers')

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
    comments = Set('Comment')
    likes = Set('Like')

class Comment(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(User)
    post = Required(Post)
    timestamp = Optional(str) # TODO
    text_content = Required(str)

class Like(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(User)
    post = Required(Post)

db.generate_mapping(create_tables=True)

app = FastAPI()

@app.get("/")
def get_root():
    return "!"

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
