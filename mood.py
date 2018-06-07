import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD
from Adafruit_IO import MQTTClient
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")

ADAFRUIT_IO_USERNAME = os.getenv("ADAFRUIT_IO_USERNAME")
ADAFRUIT_IO_KEY = os.getenv("ADAFRUIT_IO_KEY")
ADAFRUIT_IO_FEED_NAME = os.getenv("ADAFRUIT_IO_FEED_NAME")

def connected(client):
  print('Connected to Adafruit IO!  Listening for %s changes...' % ADAFRUIT_IO_FEED_NAME)
  client.subscribe(ADAFRUIT_IO_FEED_NAME)

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

def pressed(x):
    i = button_pins.index(x)
    lcd.clear()
    lcd.write_string('pressed %s' % i)
    print('button %s pressed!' % i)
    client.publish(ADAFRUIT_IO_FEED_NAME, button_values[i])
    GPIO.output(led_pins[i], True)
    time.sleep(1)
    GPIO.output(led_pins[i], False)

led_pins = 23, 12, 20, 19
button_pins = 24, 16, 21, 26
button_values = -2, -1, 1, 2

PORT_EXPANDER = 'PCF8574'
I2C_ADDRESS = 0x27
lcd = CharLCD(PORT_EXPANDER, I2C_ADDRESS)

GPIO.setmode(GPIO.BCM)
for i in range(4):
    GPIO.setup(led_pins[i], GPIO.OUT)
    GPIO.setup(button_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button_pins[i], GPIO.RISING, callback=pressed, bouncetime=100)

lcd.clear()
lcd.write_string('ready!')

while True:
    pass