import os
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
    publications = Set('Publication') # TODO
    comments = Set('Comment')
    likes = Set('Like')

class Connection(db.Entity): # TODO
    source = Required(User, reverse='following')
    destination = Required(User, reverse='followers')
    PrimaryKey(source, destination)

class Group(db.Entity):
    id = PrimaryKey(int, auto=True)
    created_by = Required(User)
    name = Required(str, unique=True)
    description = Required(str)
    publications = Set('Publication') # TODO
    
class Publication(db.Entity):
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
    publication = Required(Publication)
    timestamp = Optional(str) # TODO
    text_content = Required(str)

class Like(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(User)
    publication = Required(Publication)
    # timestamp = Optional(str)

db.generate_mapping(create_tables=True)