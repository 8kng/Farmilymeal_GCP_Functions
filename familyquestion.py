import os
import sqlalchemy

from google.cloud import storage
from click.types import File
from flask import Request, Response
from flask.helpers import make_response
from typing import Union

connection_name = os.environ['INSTANCE_CONNECTION_NAME']
db_password = os.environ['DATABASE_USER_PASSWORD']
db_name = os.environ['NAME']
db_user = os.environ['USER']
driver_name = 'mysql+pymysql'
query_string = dict({"unix_sock": "/cloudsql/{}".format(connection_name)})
def familyquestion(request: Request) -> Union[Response, None]:
    if request.method == 'POST':
        request_json = request.get_json()
        textdata = request_json['file']
        stmt = sqlalchemy.text(
            'INSERT INTO entries (guestName, content) value({0}, {1});').format("Question1", textdata)
        db = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername=driver_name,
                username=db_user,
                password=db_password,
                database=db_name,
                query=query_string,)
                ,pool_size=5,
                max_overflow=2,
                pool_timeout=30,
                pool_recycle=1800)
        try:
            with db.connect() as conn:
                conn.execute(stmt)
        except Exception as e:
            return 'error: {}'.format(str(e))
        return make_response('uploaded')
    return ('error')