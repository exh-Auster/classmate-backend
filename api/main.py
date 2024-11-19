import os

from datetime import datetime
from dateutil import parser

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import *

from api.mock_data import *

from .database import * # from .db import engine, SQLModel

# import pytz

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://eng-soft-proj.vercel.app",
    "https://classmate-front.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(__name__)

# # if __name__ == "main": # if __name__ == "__main__":
# create_db_and_tables()
# create_users()
# create_groups()

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.get("/init")
def init_db():
    create_db_and_tables()
    create_users()
    create_groups()

@app.post("/user/")
def create_user(user: User):
    with Session(engine) as session:
        # TODO: check for existing email

        session.add(user)
        session.commit()
        session.refresh(user)
        return user # TODO: check
    
@app.get("/user/{user_id}")
def get_user_by_id(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)

        if not user:
            raise HTTPException(status_code=404, detail=f"User with {user_id=} not found")

        return user
    
@app.get("/user/{user_id}/groups/")
def get_groups_by_user_id(user_id: int):
    with Session(engine) as session:
        groups = session.exec(select(Group).where(User.id == user_id)).all() # TODO: fix
        return groups

@app.get("/user/")
def get_all_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
    
@app.post("/group/")
def create_group(group: Group):
    with Session(engine) as session:
        session.add(group)
        session.commit()
        session.refresh(group)
        return group # TODO: check
    
@app.get("/group/{group_id}")
def get_group_by_id(group_id: int):
    with Session(engine) as session:
        group = session.exec(select(Group).where(Group.id == group_id)).one()
        return group
    
@app.get("/group/{group_id}/posts")
def get_posts_by_group_id(group_id: int):
    with Session(engine) as session:
        posts = session.exec(select(Post).where(Post.group_id == group_id)).all()
        return posts

@app.post("/post/")
def create_post(post: Post):
    with Session(engine) as session:
        # TODO: check for existing email

        if isinstance(post.timestamp, str):
            post.timestamp = parser.isoparse(post.timestamp)#.astimezone(pytz.timezone('America/Sao_Paulo'))

        session.add(post)
        session.commit()
        session.refresh(post)
        return post # TODO: check

@app.get("/post/{post_id}")
def get_post_by_id(post_id: int):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.id == post_id)).one()
        return post

@app.delete("/post/{post_id}")
def delete_post_by_id(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        session.delete(post)
        session.commit()

        return {"ok": True} # TODO: check

@app.get("/post/")
def get_all_posts():
    with Session(engine) as session:
        posts = session.exec(select(Post)).all()
        return posts

@app.post("/post/{post_id}/comment")
def create_comment(post_id: int, comment: Comment):
    comment.post_id = post_id

    if isinstance(comment.timestamp, str):
        comment.timestamp = parser.isoparse(comment.timestamp)#.astimezone(pytz.timezone('America/Sao_Paulo'))

    with Session(engine) as session:
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return comment
    
@app.get("/post/{post_id}/comment")
def get_comments_by_post_id(post_id: int):
    with Session(engine) as session:
        comments = session.exec(select(Comment).where(Comment.post_id == post_id)).all()
        return comments

@app.delete("/post/{post_id}/comment/{comment_id}") # TODO: check
def delete_comment_by_id(post_id: int, comment_id: int):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        session.delete(comment)
        session.commit()

        return {"ok": True} # TODO: check

@app.post("/post/{post_id}/like")
def like_post(post_id: int, like: Like):
    like.post_id = post_id # TODO: check

    if isinstance(like.timestamp, str):
            like.timestamp = parser.isoparse(like.timestamp)#.astimezone(pytz.timezone('America/Sao_Paulo'))

    with Session(engine) as session:
        session.add(like)
        session.commit()
        session.refresh(like)
        return like
    
@app.get("/post/{post_id}/like")
def get_likes_by_post_id(post_id: int):
    with Session(engine) as session:
        likes = session.exec(select(Like).where(Like.post_id == post_id)).all()
        return likes
    
@app.delete("/posts/{post_id}/like")
def remove_likes(post_id: int, like: Like):
    with Session(engine) as session:
        like = session.exec(select(Like).where(Like.post_id == post_id).where(Like.author_id == like.author_id)).one_or_none()

        if not like:
            raise HTTPException(status_code=404, detail="Like not found")
        
        session.delete(like)
        session.commit()

        return {"ok": True} # TODO: check
    
@app.get("/user/{user_id}/posts/") # TODO: CO
def get_posts_by_user_id(user_id: int):
    with Session(engine) as session:
        posts = session.exec(select(Post).where(Post.author_id == user_id)).all()
        return posts
    
@app.get("/user/{user_id}/groups/")
def get_member_groups_by_user_id(user_id: int):
    with Session(engine) as session:
        groups = session.exec(
            select(Group).join(UserGroupLink).where(UserGroupLink.user_id == user_id)
        ).all()
        return groups

@app.post("/user/{user_id}/groups/{group_id}/join")
def join_group(user_id: int, group_id: int):
    with Session(engine) as session:

        group = session.exec(select(Group).where(Group.id == group_id)).one_or_none()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        user_group_link = session.exec(
            select(UserGroupLink).where(UserGroupLink.user_id == user_id).where(UserGroupLink.group_id == group_id)
        ).one_or_none()
        if user_group_link:
            raise HTTPException(status_code=400, detail="User is already a member of the group")

        new_user_group_link = UserGroupLink(user_id=user_id, group_id=group_id)
        session.add(new_user_group_link)
        session.commit()

        return {"ok": True}