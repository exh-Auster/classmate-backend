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


app = FastAPI()

@app.get("/")
def get_root():
    return "!"