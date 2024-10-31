from datetime import datetime

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from api.models import *

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://eng-soft-proj.vercel.app",
    "*"
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

@app.get("/wipe")
def wipe_db():
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
    return {"status": "wiped"}