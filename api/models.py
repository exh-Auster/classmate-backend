import os
from datetime import datetime
from pony.orm import *

db = Database()

db.bind(provider='postgres',
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        database=os.environ["POSTGRES_DATABASE"])

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, 254, unique=True)
    password_hash = Required(str)
    registered_at = Required(datetime)
    name = Required(str, 70)
    bio = Optional(str, 240)
    groups = Set('Group', reverse='members')
    created_groups = Set('Group', reverse='created_by')
    posts = Set('Post')
    likes = Set('Like')
    comments = Set('Comment')
    following = Set('Following', reverse='follower')
    followers = Set('Following', reverse='followee')


class Group(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 25)
    description = Optional(str, 240)
    posts = Set('Post')
    members = Set(User, reverse='groups')
    created_by = Required(User, reverse='created_groups')
    creation_date = Required(datetime)


class Post(db.Entity):
    id = PrimaryKey(int, auto=True)
    group = Required(Group)
    author = Required(User)
    body = Required(str, 500)
    likes = Set('Like')
    comments = Set('Comment')
    external_content_url = Optional(str, 255)
    timestamp = Required(datetime)


class Comment(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(User)
    post = Required(Post)
    body = Required(str, 240)
    timestamp = Required(datetime)


class Like(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(User)
    post = Required(Post)
    timestamp = Required(datetime)


class Following(db.Entity):
    id = PrimaryKey(int, auto=True)
    follower = Required(User, reverse='following')
    followee = Required(User, reverse='followers')
    timestamp = Required(datetime)

db.generate_mapping(create_tables=True)