import os
import sys
import random
import time
from Adafruit_IO import MQTTClient
# import RPi.GPIO as GPIO
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")

ADAFRUIT_IO_USERNAME = os.getenv("ADAFRUIT_IO_USERNAME")
ADAFRUIT_IO_KEY = os.getenv("ADAFRUIT_IO_KEY")

redButton = 0;
yellowButton = 0;
whiteButton = 0;
blueButton = 0;
greenButton = 0;

redLight = 0;
yellowLight = 0;
whiteLight = 0;
blueLight = 0;
greenLight = 0;

def connected(client):
  print('Connected to Adafruit IO!  Listening for DemoFeed changes...')
  client.subscribe('DemoFeed')

def disconnected(client):
  print('Disconnected from Adafruit IO!')
  sys.exit(1)

def message(client, feed_id, payload, retain):
  print('Feed {0} received new value: {1}'.format(feed_id, payload))

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

client.connect()

client.loop_background()
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
    value = random.randint(0, 100)
    print('Publishing {0} to DemoFeed.'.format(value))
    client.publish('DemoFeed', value)
    time.sleep(10)


# GPIO.cleanup()