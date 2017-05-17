import RPi.GPIO as GPIO
import time

# Define pins to use
OUT_PINS = [4, 26];

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# setup all of the pins
for GPIO_Pin in OUT_PINS:
	GPIO.setup(GPIO_Pin, GPIO.OUT)

### Blink LEDs
while(1):

	# Get user input
	try:
		input = raw_input;
	except NameError:
		pass;
		
	selectedLED = input("Enter the LED to Light: ");
	
	# address will be a binary string, which will be sent to the GPIO
	# pins succesively
	LEDAddresses = str(bin(selectedLED));
	
	# write address to the GPIO pins
	for idx, currentPin in LEDAddresses:
	    
	    # Setup the MUX
		GPIO.output(OUT_PINS[idx], currentPin)
	
	print("LED on");

