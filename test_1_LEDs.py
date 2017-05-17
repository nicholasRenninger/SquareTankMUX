import RPi.GPIO as GPIO
import time
import math

# Define pins to use
OUT_PINS = [4, 26];
numAddressBits = math.ceil( math.log(len(OUT_PINS)) / math.log(2) );

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
		
	# don't take the 0b portion of 0b101...
	selectedLED = bin(int(input("Enter the LED to Light: ")))[2:];
	
	# address will be a binary string, which will be sent to the GPIO
	# pins succesively
	LEDAddresses = '%0*d' % (numAddressBits, selectedLED);
	
	# write address to the GPIO pins
	for idx, currentPin in enumerate(LEDAddresses):
	    
	    print idx, currentPin
	    #~ # Setup the MUX
	    #~ if currentPin == 1:
			#~ GPIO.output(OUT_PINS[idx], true)
		#~ else: # currentPin = 0
			#~ GPIO.output(OUT_PINS[idx], false)
			
	
	print("LED on");

