# imports
from readMKSGauge import readGauge
from setup import setupGuagePort

# set the command to read pressures from the gauge
readCmd = "@254PR4?;FF"

# find any MKS gauges attached to the computer, then open the port and return
# the serial port object. Returns an empty string if it encounters any errors
# opening the communication port to the gauge.
serPort = setupGuagePort()

# if the serial port did not open properly, then exit
if not serPort:
    exit()

shouldPrint = False

# Communicating with Device
if serPort.isOpen():

    try:
        # read from gauge until keyboard interrupt
        while True:

            (errorSTR, guageData) = readGauge(serPort, readCmd, shouldPrint)

            if not guageData:
                print('Lost contact with guage.')
                exit()

            print(guageData, "Torr")

    except KeyboardInterrupt:
        print("Exiting Reading Loop")

    # print any of the errors received from the guage
    if not errorSTR:
        print("Exited communication with no device error.")
    else:
        print("Exited communication loop with error message: ", errorSTR)

    # close serial port once the communication has stopped
    serPort.close()

else:

    print("Cannot open serial port.")
