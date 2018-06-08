import os
import sys
import time
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import pyowm
from threading import Timer
from RPLCD.i2c import CharLCD
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

from adafruitio import ioclient

ADAFRUIT_IO_MOOD_FEED_NAME = os.getenv("ADAFRUIT_IO_MOOD_FEED_NAME")
ADAFRUIT_IO_TEMP_FEED_NAME = os.getenv("ADAFRUIT_IO_TEMP_FEED_NAME")
ADAFRUIT_IO_HUMID_FEED_NAME = os.getenv("ADAFRUIT_IO_HUMID_FEED_NAME")

def publishDhtData():
    humidity,temperature = dht.read_retry(dht.DHT22, 4)
    ioclient.publish(ADAFRUIT_IO_TEMP_FEED_NAME, temperature)
    ioclient.publish(ADAFRUIT_IO_HUMID_FEED_NAME, humidity)

def light_off(x):
    GPIO.output(led_pins[x], False)

def pressed(x):
    global last_press
    if time.time() - last_press < 5:
        return
    last_press = time.time()
    i = button_pins.index(x)
    lcd.clear()
    lcd.write_string('pressed %s' % i)
    print('button %s pressed!' % i)
    ioclient.publish(ADAFRUIT_IO_MOOD_FEED_NAME, button_values[i])

    GPIO.output(led_pins[i], True)
    Timer(1, light_off, args=[i]).start()

    publishDhtData()

led_pins = 23, 12, 20, 19
button_pins = 24, 16, 21, 26
button_values = -2, -1, 1, 2
last_press = 0

PORT_EXPANDER = 'PCF8574'
I2C_ADDRESS = 0x27
lcd = CharLCD(PORT_EXPANDER, I2C_ADDRESS)

GPIO.setmode(GPIO.BCM)
for i in range(4):
    GPIO.setup(led_pins[i], GPIO.OUT)
    GPIO.setup(button_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button_pins[i], GPIO.FALLING, callback=pressed, bouncetime=100)

lcd.clear()
lcd.write_string('ready!')

while True:
    try:
        pass
    except:
        print('cleaning up!')
        GPIO.cleanup()

