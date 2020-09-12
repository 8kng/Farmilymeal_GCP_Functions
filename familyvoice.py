import os

from google.cloud import storage
from click.types import File
from flask import Request, Response
from flask.helpers import make_response
from typing import Union

FAMILY_ANSEWR = os.environ['FAMILY_ANSEWR']

def hello_world(request: Request) -> Union[Response, None]:
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'POST':
        sound_file = request.files.get('file')
        if sound_file == None:
            return make_response('Bad Request', 400)
        gcs = storage.Client()
        bucket = gcs.get_bucket(FAMILY_ANSEWR)
        blob = bucket.blob(sound_file.filename)
        blob.upload_from_string(sound_file.read(), content_type=sound_file.content_type)
        return make_response(blob.public_url, 201)
    mmake_response('Error', 500)