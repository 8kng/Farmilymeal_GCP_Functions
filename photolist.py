import os
import sqlalchemy
import flask import json

from google.cloud import storage
from click.types import File
from flask import Request, Response
from flask.helpers import make_response
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc
import datetime

meal_phot = os.environ['meal_phot']
connection_name = os.environ['INSTANCE_CONNECTION_NAME']
db_password = os.environ['DATABASE_USER_PASSWORD']
db_name = os.environ['NAME']
db_user = os.environ['USER']
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})
Base = declarative_base()

def photolist(request: Request) -> Union[Response, None]:
    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername = driver_name,
            username = db_user,
            password = db_password,
            database = db_name,
            query = query_string,
        ),
        pool_size = 5,
        max_overflow = 2,
        pool_timeout = 30,
        pool_recycle = 1800
    )
    SessionClass = sessionmaker(engine) 
    session = SessionClass()

    if request.method == 'GET':
        photos = session.query(Photo)
            .order_by(desc(Photo.datetime))
            .limit(20)
            .all()
        response_data = {}
        response_data["photos"] = photos

        return make_response(json.dump(response_data), {'Content-Type': 'application/json'})

    elif request.method == 'POST':
        request_json = request.get_json()
        newphoto = request_json['madakimetenai']
        now_datetime = datetime.datetime.now()

        new_url = "https://storage.cloud.google.com/meal_phot/{}".format(newphoto)
        photo_add = Photo(url = new_url, datetime = now_datetime)
        session.add(photo_add)
        session.commit()

        return make_response("201 uploaded", 201)

class Photo(Base):
    __tablename__="photo"
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    datetime = Column(DateTime)
