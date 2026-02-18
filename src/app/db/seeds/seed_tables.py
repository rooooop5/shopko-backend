import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv(".env")
# -----url of the database from the .env------
url = os.getenv("DATABASE_URL")

# -----create the database engine-----
engine = create_engine(url)


def create_tables():
    print(os.getcwd())
    print(os.getenv("DATABASE_URL"))
    SQLModel.metadata.create_all(engine)
