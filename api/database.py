from sqlmodel import *

from .models import *

engine = create_engine(sqlite_url, echo=True)  

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine) 