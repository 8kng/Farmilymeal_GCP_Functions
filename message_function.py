import os
import sqlalchemy
import datetime

from flask import json
from flask import Flask
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

connection_name = os.environ['INSTANCE_CONNECTION_NAME']
db_password = os.environ['DATABASE_USER_PASSWORD']
db_name = os.environ['DB_NAME']
db_user = os.environ['USER']
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})
Base = declarative_base()
ma = Marshmallow()

def message_function(request: Request) -> Union[Response, None]:
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
    
    if request.method == 'POST':
        request_json = request.get_json()
        get_text = request_json['text']
        get_kind = request_json['kind']

        text_add = Message(text = get_text, kind = get_kind)
        session.add(text_add)
        session.commit()

        return make_response('201 uploaded', 201)

    elif request.method == 'GET':
        response_date = {}
        texts = session.query(Message)\
            .order_by(desc(Message.id))\
            .limit(20)\
            .all()
        response_date = jsonify({'texts': MessageSchema(many = True).dump(texts)})
        response = make_response(response_date)
        response.headers['Content-Type'] = 'application/json'
        return response

class Message(Base):
    __tablename__="message"
    id = Column(Integer, primary_key=True)
    text = Column(String(255))
    kind = Column(String(255))

class MessageSchema(ma.ModelSchema):
    class Meta:
        model = Message