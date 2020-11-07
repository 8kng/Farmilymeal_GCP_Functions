import time
import json
import requests
import picamera
import datetime
import urllib.request
import urllib.parse
from PIL import Image
from io import BytesIO

now = datetime.datetime.now()
date = now.strftime("%Y%m%d")
hour = now.hour

if (1 <= hour <= 12):
    date += "_1.jpeg"
elif (12 <= hour <= 15):
    date += "_2.jpeg"
else:
    date += "_3.jpeg"

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.vflip = True
    camera.hflip = True
    camera.start_preview()
    time.sleep(2)
    camera.capture(date)

url = "https://asia-northeast1-farmily-meal.cloudfunctions.net/photolist"
pho = Image.open(date)
date = {"madakimetenai": pho, "name": date}
headers = {"content-type": "applocation/json"}

res = requests.post(url, headers = headers, data = data)
print(res.json())
print (date)