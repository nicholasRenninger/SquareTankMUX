from __future__ import print_function
import RPi.GPIO as GPIO
import math

# Define pins to use
pinA = 4
pinB = 26
OUT_PINS = [pinB, pinA]
MAX_NUM_ADDRESSES = 4  # CD4052
numAddressBits = int(math.ceil(math.log(MAX_NUM_ADDRESSES) / math.log(2)))

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# setup all of the pins
for GPIO_Pin in OUT_PINS:
    GPIO.setup(GPIO_Pin, GPIO.OUT)

# Blink LEDs
while(1):

    # Get user input
    try:
        input = raw_input()
    except NameError:
        pass

    # don't take the 0b portion of 0b101...
    selectedLED = int(input("Enter the LED to Light: "))

    # address will be a binary string, which will be sent to the GPIO
    # pins succesivelypassword

    LEDAddress = '%0*d' % (numAddressBits, int(bin(selectedLED)[2:]))

    # write address to the GPIO pins
    for idx, currentPin in enumerate(LEDAddress):

        print("current pin = ", currentPin)
        # Setup the MUX
        if (currentPin == "1"):
            GPIO.output(OUT_PINS[idx], GPIO.HIGH)
            print(OUT_PINS[idx], "is high")
        else:
            # currentPin = 0
            print(OUT_PINS[idx], "is low")
            GPIO.output(OUT_PINS[idx], GPIO.LOW)

    print("LED on")
