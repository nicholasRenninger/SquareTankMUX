import RPi.GPIO as GPIO
import time
import math

# Define pins to use
OUT_PINS = [4, 26];
MAX_NUM_ADDRESSES = 4; # CD4052
numAddressBits = int(math.ceil( math.log(MAX_NUM_ADDRESSES) / math.log(2) ));

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
	selectedLED = int(input("Enter the LED to Light: "));
	#~ print selectedLED
	#~ print numAddressBits
	
	# address will be a binary string, which will be sent to the GPIO
	# pins succesively
	LEDAddress = '%0*d' % (numAddressBits, int(bin(selectedLED)[2:]));
	#~ print LEDAddress
	
	# write address to the GPIO pins
	for idx, currentPin in enumerate(LEDAddress):
	    
	    #~ print idx, currentPin
		# Setup the MUX
		if (currentPin == 1):
			GPIO.output(OUT_PINS[idx], True)
		else:
			# currentPin = 0
			GPIO.output(OUT_PINS[idx], False)
			
	
	print("LED on");

