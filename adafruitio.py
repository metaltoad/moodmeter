import os
import sys
from Adafruit_IO import MQTTClient

ADAFRUIT_IO_USERNAME = os.getenv("ADAFRUIT_IO_USERNAME")
ADAFRUIT_IO_KEY = os.getenv("ADAFRUIT_IO_KEY")
ADAFRUIT_IO_MOOD_FEED_NAME = os.getenv("ADAFRUIT_IO_MOOD_FEED_NAME")
ADAFRUIT_IO_TEMP_FEED_NAME = os.getenv("ADAFRUIT_IO_TEMP_FEED_NAME")
ADAFRUIT_IO_HUMID_FEED_NAME = os.getenv("ADAFRUIT_IO_HUMID_FEED_NAME")

def connected(client):
  print('Connected to Adafruit IO! Listening for feed changes...')
  client.subscribe(ADAFRUIT_IO_MOOD_FEED_NAME)
  client.subscribe(ADAFRUIT_IO_TEMP_FEED_NAME)
  client.subscribe(ADAFRUIT_IO_HUMID_FEED_NAME)

def disconnected(client):
  print('Disconnected from Adafruit IO!')
  sys.exit(1)

def message(client, feed_id, payload, retain):
  print('Feed {0} received new value: {1}'.format(feed_id, payload))

ioclient = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

ioclient.on_connect    = connected
ioclient.on_disconnect = disconnected
ioclient.on_message    = message

ioclient.connect()

ioclient.loop_background()