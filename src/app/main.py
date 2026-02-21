from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.startup import initialise_database
from app.router.auth_router import auth_router
@asynccontextmanager
async def life(app:FastAPI):
    initialise_database()
    yield
    print("Shutting down api.\n")

app=FastAPI(lifespan=life)

@app.get("/")
def entry():
    return {"Hi":"This is the entry page."}

app.include_router(auth_router)