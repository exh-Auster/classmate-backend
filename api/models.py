import os

from datetime import datetime

from pydantic import EmailStr
from sqlmodel import *

class UserGroupLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True) # TODO: None?
    group_id: int | None = Field(default=None, foreign_key="group.id", primary_key=True) # TODO: None?

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # email: str = Field(unique=True) # Required(str, 254, unique=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password_hash: str # Required(str)
    registered_at: datetime = datetime.now() # Required(datetime)
    name: str # Required(str, 70)
    bio: str # Optional(str, 240)
    groups: list["Group"] | None = Relationship(back_populates="members", link_model=UserGroupLink) # Set('Group', reverse='members')
    created_groups: list["Group"] | None = Relationship(back_populates="created_by") # Set('Group', reverse='created_by')
    posts: list["Post"] | None = Relationship(back_populates="author") # Set('Post')
    likes: list["Like"] | None = Relationship(back_populates="author") # Set('Like')
    bookmarks: list["Bookmark"] | None = Relationship(back_populates="author")
    comments: list["Comment"] | None = Relationship(back_populates="author") # Set('Comment')
    following: list["Following"] | None = Relationship(back_populates="follower") # Set('Following', reverse='follower')
    followers: list["Following"] | None = Relationship(back_populates="followee") # Set('Following', reverse='followee')

class Group(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str # Required(str, 25)
    description: str | None = None # Optional(str, 240)
    posts: list["Post"] | None = Relationship(back_populates="group") # Set('Post')
    members: list["User"] | None = Relationship(back_populates="groups", link_model=UserGroupLink) # Set(User, reverse='groups') | TODO: None?
    creation_date: datetime = datetime.now() # Required(datetime)

    creator_id: int = Field(default=None, foreign_key="user.id")
    created_by: User = Relationship(back_populates="created_groups") # Required(User, reverse='created_groups')

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    body: str # Required(str, 500)
    likes: list["Like"] | None = Relationship(back_populates="post") # Set('Like')
    bookmarks: list["Bookmark"] | None = Relationship(back_populates="post")
    comments: list["Comment"] | None = Relationship(back_populates="post") # Set('Comment')
    external_content_url: str | None # Optional(str, 255)
    timestamp: datetime # Required(datetime)

    author_id: int = Field(default=None, foreign_key="user.id")
    author: User = Relationship(back_populates="posts") # Required(User)

    group_id: int = Field(default=None, foreign_key="group.id")
    group: Group = Relationship(back_populates="posts") # Required(Group)

class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    body: str # Required(str, 240)
    timestamp: datetime = datetime.now() # Required(datetime)

    author_id: int = Field(default=None, foreign_key="user.id")
    author: User = Relationship(back_populates="comments") # Required(User)

    post_id: int | None = Field(default=None, foreign_key="post.id")
    post: Post = Relationship(back_populates="comments") # Required(Post)

# class Like(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True) # TODO: composite?
#     timestamp: datetime = datetime.now() # Required(datetime)

#     author_id: int = Field(default=None, foreign_key="user.id")
#     author: User = Relationship(back_populates="likes") # Required(User)

#     post_id: int = Field(default=None, foreign_key="post.id")
#     post: Post = Relationship(back_populates="likes") # Required(Post)

class Like(SQLModel, table=True):
    author_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    post_id: int = Field(default=None, foreign_key="post.id", primary_key=True)
    timestamp: datetime = datetime.now()

    author: User = Relationship(back_populates="likes")
    post: Post = Relationship(back_populates="likes")

    class Config:
        table_args = (PrimaryKeyConstraint('author_id', 'post_id'),)

class Bookmark(SQLModel, table=True):
    author_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    post_id: int = Field(default=None, foreign_key="post.id", primary_key=True)
    timestamp: datetime = datetime.now()

    author: User = Relationship(back_populates="bookmarks")
    post: Post = Relationship(back_populates="bookmarks")

    class Config:
        table_args = (PrimaryKeyConstraint('author_id', 'post_id'),)

class Following(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) # TODO: composite?
    timestamp: datetime = datetime.now() # Required(datetime)

    user_id: int = Field(default=None, foreign_key="user.id") # TODO: check
    follower: User = Relationship(back_populates="following") # Required(User, reverse='following')
    followee: User = Relationship(back_populates="followers") # Required(User, reverse='followers')