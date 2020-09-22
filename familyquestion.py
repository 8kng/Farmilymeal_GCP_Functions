import os
import sqlalchemy

from google.cloud import storage
from flask import Request, Response
from flask.helpers import make_response
from typing import Union
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
Base = declarative_base()


def familyquestion(request: Request) -> Union[Response, None]:
    if request.method == 'POST':
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

        request_json = request.get_json()
        textdata = request_json['file']
        id = request_json['id']

        questionadd = session.query(Question).filter(
            Question.id == id).first()
        questionadd.content = textdata
        session.commit()

        return make_response("201 Created", 201)


class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    text = Column(String(255))
