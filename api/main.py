import os
from fastapi import FastAPI
from pony.orm import *
from pydantic import BaseModel
from datetime import date

# db = PostgresqlDatabase(os.environ["POSTGRES_DATABASE"],
#                            user=os.environ["POSTGRES_USER"],
#                            password=os.environ["POSTGRES_PASSWORD"],
#                            host=os.environ["POSTGRES_HOST"],
#                            port=5432)

db = Database()

class User(db.Entity):
    name = Required(str)

db.bind(provider='postgres', user=os.environ["POSTGRES_USER"], password=os.environ["POSTGRES_PASSWORD"], host=os.environ["POSTGRES_HOST"], database=os.environ["POSTGRES_DATABASE"])

app = FastAPI()

@app.get("/")
def get_root():
    return "!"

@app.get("/db_test")
def db_test():
    db.generate_mapping(create_tables=True)

    return "!"