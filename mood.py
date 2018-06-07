import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD

def pressed(x):
    i = button_pins.index(x)
    lcd.clear()
    lcd.write_string('pressed %s' % i)
    print('button %s pressed!' % i)
    GPIO.output(led_pins[i], True)
    time.sleep(1)
    GPIO.output(led_pins[i], False)

led_pins = 23, 12, 20, 19
button_pins = 24, 16, 21, 26

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
