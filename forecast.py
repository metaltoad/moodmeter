import os
import time
import pyowm
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")
from adafruitio import ioclient

OWM_API_KEY = os.getenv("OWM_API_KEY")
ADAFRUIT_IO_OUTSIDE_TEMP_FEED_NAME = os.getenv("ADAFRUIT_IO_OUTSIDE_TEMP_FEED_NAME")
ADAFRUIT_IO_OUTSIDE_HUMID_FEED_NAME = os.getenv("ADAFRUIT_IO_OUTSIDE_HUMID_FEED_NAME")
ADAFRUIT_IO_OUTSIDE_SUNLIGHT_HOURS_FEED_NAME= os.getenv("ADAFRUIT_IO_OUTSIDE_SUNLIGHT_HOURS_FEED_NAME")
ADAFRUIT_IO_OUTSIDE_CLOUDCOVER_FEED_NAME = os.getenv("ADAFRUIT_IO_OUTSIDE_CLOUDCOVER_FEED_NAME")

owm = pyowm.OWM(OWM_API_KEY)

while True:
    observation = owm.weather_at_place('Portland,OR,USA')
    weather = observation.get_weather()
    humidity = weather.get_humidity()
    temperature = weather.get_temperature('celsius')['temp']
    sunlightHours = ((weather.get_sunset_time()-weather.get_sunrise_time())/60)/60
    # weather.get_rain()
    cloudCover = weather.get_clouds()
    ioclient.publish(ADAFRUIT_IO_OUTSIDE_TEMP_FEED_NAME, temperature)
    ioclient.publish(ADAFRUIT_IO_OUTSIDE_HUMID_FEED_NAME, humidity)
    ioclient.publish(ADAFRUIT_IO_OUTSIDE_SUNLIGHT_HOURS_FEED_NAME, sunlightHours)
    ioclient.publish(ADAFRUIT_IO_OUTSIDE_CLOUDCOVER_FEED_NAME, cloudCover)
    time.sleep(1800)