from sqlmodel import *

from sqlalchemy.engine import URL

from .models import *

postgres_url_object = URL.create(
    "postgresql",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"],
    database=os.environ["POSTGRES_DATABASE"],
)

# sqlite_file_name = "database.db"  
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# sqlite_url = os.environ["POSTGRES_URL"]

engine = create_engine(postgres_url_object, echo=True)

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)