import os
from sqlmodel import SQLModel, create_engine
from app.auth.settings import Settings

# -----url of the database from the .env through the Settings object------
url = Settings.DATABASE_URL

# -----create the database engine-----
engine = create_engine(url)


def create_tables():
    SQLModel.metadata.create_all(engine)
