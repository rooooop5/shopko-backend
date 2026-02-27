import os
from sqlmodel import SQLModel, create_engine, Session
from app.auth.settings import Settings

# -----url of the database from the .env through the Settings object------
url = Settings.DATABASE_URL

# -----create the database engine-----
engine = create_engine(url)


def create_tables():
    SQLModel.metadata.create_all(engine)

def delete_tables():
    SQLModel.metadata.drop_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session
