import Rpi.GPIO as GPIO
import time

# Define pins to use
OUT_PIN1 = 4;
OUT_PIN2 = 26;

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(OUT_PIN1, GPIO.OUT)
GPIO.setup(OUT_PIN2, GPIO.OUT)

### Blink LEDs

while(1):

    # Get user input
    try:
        input = raw_input;
    except NameError:
        pass;

    selectedPort = input("Enter the LED to Light");


    # Setup the MUX

