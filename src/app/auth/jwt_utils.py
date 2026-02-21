import os
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from pydantic import BaseModel
from dotenv import load_dotenv
from app.db.seeds.seed_tables import engine
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/token")

class Token(BaseModel):
    access_token:str
    token_type:str

load_dotenv(".env")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")


def create_access_token(data:dict):
    to_encode=data.copy()
    token=jwt.encode(payload=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return token

def authenticate_user(session:Session,token=Depends(oauth2_scheme)):
    try:
        decoded=jwt.decode(token,SECRET_KEY,ALGORITHM)
    except:
        print("Unauthorized.\n")

with Session(engine) as session:
    authenticate_user(session)