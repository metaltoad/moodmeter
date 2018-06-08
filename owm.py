import os
import pyowm
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

OWM_API_KEY = os.getenv("OWM_API_KEY")

owm = pyowm.OWM(OWM_API_KEY)

observation = owm.weather_at_place('Portland,OR,USA')
w = observation.get_weather()
print(w)                      # <Weather - reference time=2013-12-18 09:20,
                              # status=Clouds>

# Weather details
print(w.get_humidity())              # 87
print(w.get_temperature('celsius')['temp'])  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
print(w.get_sunset_time()-w.get_sunrise_time())