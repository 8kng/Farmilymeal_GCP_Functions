import os
import sqlalchemy

from google.cloud import storage
from click.types import File
from flask import Request, Response
from flask.helpers import make_response
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base

connection_name = os.environ['INSTANCE_CONNECTION_NAME']
db_password = os.environ['DATABASE_USER_PASSWORD']
db_name = os.environ['NAME']
db_user = os.environ['USER']
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})
Base=declarative_base()

def familyquestion(request: Request) -> Union[Response, None]:
    engine = create_engine('farmily-meal:asia-northeast1:questions')
    SessionClass=sessionmaker(engine) 
    session=SessionClass()
    request_json = request.get_json()
    textdata = request_json['file']
    questiona=User(guestName="Question1", content=textdata)
    session.add(questiona)
    session.commit()
    return ('finish')

    class User(Base):
        _tablename_="question"
        question_id=Column(Integer, primary_key=True)
        guestName=Column(String(255))
        content=Column(String(255))