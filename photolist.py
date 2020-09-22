import os
from flask import json
import sqlalchemy

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
    SessionClass = sessionmaker(engine)
    session = SessionClass()

    if request.method == 'GET':
        # desc で降順に(大きいもの→小さいもの)
        # 大きい日時→小さい日時(新しい順)
        # limit で個数を指定
        photos = session.query(Photo) \
            .order_by(desc(Photo.datetime)) \
            .limit(20) \
            .all()

        # JSON にするときに値に名前をつけてあげないといけないので
        # 空辞書を作って photos というキーに photos を入れている
        response_data = {}
        response_data["photos"] = photos

        # json.dumps で object を JSON の文字列に変換する
        return make_response(json.dumps(response_data), {'Content-Type': 'application/json'})

    elif request.method == 'POST':
        request_json = request.get_json()
        newphoto = request_json['madakimetenai']
        for i in range(1, 19):
            n = i + 1
            listchange = session.query(User).filter(User.entryId == n).first()
            listchange.photourl = photourllist[i]
            listchange.date = datelist[i]
            session.commit()
        listset = session.query(User).filter(User.entryId == 1).first()
        listset.photourl = "https://storage.cloud.google.com/meal_phot/{}".format(
            newphoto)
        listset.date = "{0}/{1}/{2}/{3}:{4}".format(
            dt_now.year, dt_now.month, dt_now.dat, dt_now.hour.dt.minute)
        session.commit()
        return make_response('POST')


class Photo(Base):
    __tablename__ = "photo"
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    datetime = Column(DateTime)
