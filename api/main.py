import os

from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "http://localhost:3000",
    "https://eng-soft-proj.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.get("/user/{user_id}")
@db_session
def get_user_by_id(user_id: int):
    if User.exists(id=user_id):
        return User[user_id]
    else:
        raise HTTPException(
            status_code = 404, detail = f"User with {user_id=} does not exist."
    )

@app.get("/group/{group_id}")
@db_session
def get_group_by_id(group_id: int):
    if Group.exists(id=group_id):
        return Group[group_id]
    else:
        raise HTTPException(
            status_code = 404, detail = f"Group with {group_id=} does not exist."
    )

@app.get("/post/{post_id}")
@db_session
def get_post_by_id(post_id: int):
    if Post.exists(id=post_id):
        return Post[post_id]
    else:
        raise HTTPException(
            status_code = 404, detail = f"Post with {post_id=} does not exist."
    )

@app.post("/post")
@db_session
def create_post(post_data: dict):
    Post(
        author=post_data["author_id"],
        group=post_data["group_id"],
        timestamp=datetime.now().isoformat(), # TODO
        text_content=post_data["text_content"],
        external_content_url=post_data.get("external_content_url")
    )

    return {"status": "ok"} # TODO

@app.delete("/post/{post_id}")
@db_session
def delete_post(post_id: int):
    if Post.exists(id=post_id):
        Post[post_id].delete()

        return {"status": "ok"} # TODO
    else:
        raise HTTPException(
            status_code = 404, detail = f"Post with {post_id=} does not exist."
    )

@app.post("/comment")
@db_session
def create_comment(comment_data: dict):
    Comment(
        author=comment_data["author_id"],
        post=comment_data["post_id"],
        timestamp=datetime.now().isoformat(), # TODO
        text_content=comment_data["text_content"]
    )

    return {"status": "ok"} # TODO

@app.delete("/comment/{comment_id}")
@db_session
def delete_comment(comment_id: int):
    if Comment.exists(id=comment_id):
        Comment[comment_id].delete()
        return {"status": "ok"} # TODO
    else:
        raise HTTPException(
            status_code = 404, detail = f"Comment with {comment_id=} does not exist."
    )

@app.post("/like")
@db_session
def like_post(like_data: dict):
    Like(
        author=like_data["author_id"],
        post=like_data["post_id"],
        timestamp=datetime.now().isoformat(), # TODO
    )

    return {"status": "ok"} # TODO

@app.post("/follow")
@db_session
def follow_user(connection_data: dict):
    Connection(
        source=connection_data["source"],
        destination=connection_data["destination"],
    )

    return {"status": "ok"} # TODO

@app.delete("/follow/{user_id}")
@db_session
def unfollow(connection_id: int):
    Connection[connection_id].delete() # TODO

    return {"status": "ok"} # TODO