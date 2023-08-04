import os
import secrets

from dotenv import load_dotenv
from typing_extensions import Annotated
from psycopg2.errors import UniqueViolation
from pymongo import MongoClient

from fastapi_sqlalchemy import db
from fastapi import HTTPException, status, APIRouter, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder


from ..models import User, Profile
from ..schemas import UserSchema

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


# To declare the location of the env file inside the docker container
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR.replace("/app/routers", ""), ".env"))


# Initializing the conection with the MongoDB server using pymongo driver
MongoClient = MongoClient(os.environ["MONGO_URL"])
mongoDB = MongoClient.fast;


# Initializing APIRouter
router = APIRouter()


@router.post('/signup/',status_code=status.HTTP_201_CREATED)
def signup(user: UserSchema):
    """Method to sign up user and create user instance in postgreSQL database table"""

    user = User(**user.dict())
    db.session.add(user)

    try:
        db.session.commit()

    # To check email or phone already exists or not
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        raise HTTPException(status_code=400, detail="email or phone already exists. Try with a different one")
    
    return{'message': 'User created', 'user_id':user.id}


@router.post('/upload/',status_code=status.HTTP_200_OK)
def upload(file : UploadFile, database: Annotated[str, Form()]= ..., email: Annotated[str, Form()]= ...):
    """ Method to upload the profile picture of a registered user using email of that particlar user.
        queryparamater is used to select the database for uploading between PostgreSQL and MongoDB """
    
    # Creating a file at static directory location and storing the uploaded image content in that file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filepath = BASE_DIR.replace("/routers", "")+"/static/images/"
    if file.filename.split(".")[1] not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=400, detail="Image format not acceptable")
    
    filename = secrets.token_hex(10)+"."+ file.filename.split(".")[1]
    url = filepath + filename
    file_content = file.file.read()

    with open(url, "wb") as file:
        file.write(file_content)
        
    user = db.session.query(User).filter(User.email==email).first()

    # To upload into PostgreSQL
    if database == "P":
        profile = Profile(user_id=user.id, profile_picture=url)
        db.session.add(profile)
        db.session.commit()

    # To upload into MongoDB
    elif database == "M":
        mongo_profile = {"user_id":str(user.id), "profile_picture": url}
        mongo_profile = jsonable_encoder(mongo_profile)
        mongoDB["profile"].insert_one(mongo_profile)
    
    else:
        raise HTTPException(status_code=400, detail="Value must be either P or M")

    return {"message": "file uploaded"}


@router.get('/details/{email}/', status_code=status.HTTP_200_OK)
def userDetails(email: str):
    """ To retrieve the user details from the database"""

    user = db.session.query(User).filter(User.email==email).first()
    profile = db.session.query(Profile).filter(Profile.user_id==user.id).first()


    if not user:
        raise HTTPException(status_code=404, detail="User with this email does not exists")
    
    return {"full_name": user.full_name, "email": user.email, "phone": user.phone, "profile_picture": FileResponse(profile.profile_picture)}