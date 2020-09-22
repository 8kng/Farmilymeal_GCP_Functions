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

meal_phot = os.environ['meal_phot']
connection_name = os.environ['INSTANCE_CONNECTION_NAME']
db_password = os.environ['DATABASE_USER_PASSWORD']
db_name = os.environ['NAME']
db_user = os.environ['USER']
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})
Base=declarative_base()

def photolist(request: Request) -> Union[Response, None]:
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername=driver_name,
            username=db_user,
            password=db_password,
            database=db_name,
            query=query_string,
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )
    SessionClass=sessionmaker(engine) 
    session=SessionClass()
    photourllist = dict
    datelist = dict
    for i in range(1, 20):
        listchange = session.query(User).filter(User.entryId==n).first()
        photourllist[i] = listchange.photourl
        datelist[i] = listchange.date

    if request.method == 'GET':
        photores = make_response(photolist, {'Content-Type': 'application/json'})
        dateres = make_response(datelist, {'Content-Type':'application/json'})
        return (photores, dateres)
     
    elif request.method == 'POST':
        request_json = request.get_json()
        newphoto = request_json['madakimetenai']
        for i in range(1, 19):
            n = i + 1
            listchange = session.query(User).filter(User.entryId==n).first()
            listchange.photourl = photourllist[i]
            listchange.date = datelist[i]
            session.commit()
        listset = session.query(User).filter(User.entryId==1).first()
        listset.photourl = "https://storage.cloud.google.com/meal_phot/{}".format(newphoto)
        listset.date = "{0}/{1}/{2}/{3}:{4}".format(dt_now.year, dt_now.month, dt_now.dat, dt_now.hour.dt.minute)
        session.commit()
        return make_response('POST')

class User(Base):
    __tablename__="photolist"
    entryId=Column(Integer, primary_key=True)
    photourl=Column(String(255))
    date=Column(String(255))
