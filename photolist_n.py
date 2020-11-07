import os
import logging
import sqlalchemy
import datetime
import sys
import qrcode
import io
import tempfile

from flask import escape, helpers
from flask import json
from flask import Flask
from flask import Flask, request
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
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from flask import jsonify # <- `jsonify` instead of `json` 

meal_phot = os.environ['STRAGE_NAME']
connection_name = os.environ['INSTANCE_CONNECTION_NAME']
db_password = os.environ['DATABASE_USER_PASSWORD']
db_name = os.environ['DB_NAME']
db_user = os.environ['USER']
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})
Base = declarative_base()
ma = Marshmallow()

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
    
    if request.method == 'GET':
        response_data = {}
        photos = session.query(Photo) \
            .order_by(desc(Photo.datetime)) \
            .limit(20) \
            .all()
        response_data = jsonify({'photos': PhotoSchema(many = True).dump(photos)})
        response = make_response(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response

    elif request.method == 'POST':
        request_json = request.get_json()
        name = request_json['name']
        new_photo = request.files.get['photo']
        name = request_json['name']
        if new_photo == None:
            return make_response('Bad Request', 400)

        gcs = storage.Client()
        bucket = gcs.get_bucket(meal_phot)
        blob = bucket.blob(new_photo.name)
        blob.upload_from_string(new_photo.read(), content_type=new_photo.content_type)

        return make_response("201 uploaded", 201)
        
class Photo(Base):
    __tablename__="photo"
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    datetime = Column(DateTime)

class PhotoSchema(ma.ModelSchema):
    class Meta:
        model = Photo
