import os
import sys
import random
import time
from functools import partial
from Adafruit_IO import MQTTClient
# import RPi.GPIO as GPIO
from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')

ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME')
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY')
ADAFRUIT_FEED_NAME = os.getenv('ADAFRUIT_FEED_NAME')

red = 'red'
yellow = 'yellow'
blue = 'blue'
green = 'green'
name = 'name'
value = 'value'
buttonPin = 'buttonPin'
lightPin = 'lightPin'
handler = 'handler'

# def noop():
#   pass

# class Button(object):
#   name = ""
#   value = 0
#   buttonPin = 0
#   lightPin: 0
#   handler: noop

buttons = {
  red: {
    name: red,
    value: -2,
    buttonPin: 0,
    lightPin: 0,
  },
  yellow: {
    name: yellow,
    value: -1,
    buttonPin: 0,
    lightPin: 0,
  },
  blue: {
    name: blue,
    value: 1,
    buttonPin: 0,
    lightPin: 0,
  },
  green: {
    name: green,
    value: 2,
    buttonPin: 0,
    lightPin: 0,
  }
}

def handleButtonPress(button):
  print('Pressed {0} button!'.format(button[name]))
  client.publish(ADAFRUIT_FEED_NAME, button[value])

def registerButtonEvent(button):
  print('boop'.format(button[name]))
  # GPIO.add_event_detect(button[buttonPin], GPIO.RISING, callback=button[handler])

for button in buttons:
  # print('Creating {0} button handler...'.format(button[name]))
  handler = partial(handleButtonPress, button)
  button[handler] = handler
  print('Assigning {0} button handler to pin {1}'.format(button[name], button[buttonPin]))
  registerButtonEvent(button)

# buttons[red][handler] = partial(handleButtonPress, buttons[red])
# buttons[yellow][handler] = partial(handleButtonPress, buttons[yellow])
# buttons[blue][handler] = partial(handleButtonPress, buttons[blue])
# buttons[green][handler] = partial(handleButtonPress, buttons[green])


def connected(client):
  print('Connected to Adafruit IO! Listening for {0} changes...'.format(ADAFRUIT_FEED_NAME))
  client.subscribe(ADAFRUIT_FEED_NAME)

def disconnected(client):
  print('Disconnected from Adafruit IO!')
  sys.exit(1)

def messageReceived(client, feed_id, payload, retain):
  print('Feed {0} received new value: {1}'.format(feed_id, payload))

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = messageReceived
client.connect()

# client.loop_background()
# print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
# while True:
#     value = random.randint(0, 100)
#     print('Publishing {0} to {1}.'.format(value, ADAFRUIT_FEED_NAME))
#     client.publish('DemoFeed', value)
#     time.sleep(10)


# GPIO.cleanup()