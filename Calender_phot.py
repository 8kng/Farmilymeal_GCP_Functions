import os

from google.cloud import storage
from click.types import File
from flask import Request, Response
from flask.helpers import make_response
from typing import Union

meal_phot = os.environ['meal_phot']

def calendar_photo(request: Request) -> Union[Response, None]:
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    datedata = request_json['date']
    filename = datedata + ".jpeg"

    gcs = storage.Client()
    bucket = gcs.get_bucket(meal_phot)
    none = "Noimage.jpg"

    blob = bucket.get_blob(filename)
    if (blob == None):
        blob = bucket.get_blob(none)
        photo = blob
        return (photo)
    photo = blob
    return (photo)