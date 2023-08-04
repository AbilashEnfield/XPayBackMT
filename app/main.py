import os
import uvicorn

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
from app.routers import users

# to get the base directory inside the docker container 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR.replace("/app/routers", ""), ".env"))

#initializing FastAPI
app = FastAPI()

# Adding PostgresQL connection url to DBSessionMiddleware
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# To let the FastAPI know the static folder location
app.mount("/static", StaticFiles(directory=BASE_DIR+"/static"), name="static")

# CROS settings are provided here
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:8000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# To let the FastAPI to detect the router folder and APIRouter methods inside modules in that folder
app.include_router(users.router, tags=['Users'], prefix='/api/users')


# Function to test fastapi running status
@app.get('/')
def root():
    return {'message':'FastAPI server started'}
