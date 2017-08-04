#!/usr/bin/env python

""" Enables serial communication with MKS pressure gauges.

Auto-detects the serial port the guage uses, configures the guage properly,
error checks the entire process, and then records the pressures and timestamps
in a .csv file.
"""

__author__ = "Nicholas Renninger"
__copyright__ = "'Copyright' 2017, LASP"
__credits__ = ["Liam O'Swagger"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Renninger"
__email__ = "nicholas.renninger@colorado.edu"
__status__ = "Testing"


########################################################################
# ----- Imports ----- #
from readMKSGauge import readGauge
from setup import setupGuagePort
from openCSV import openSaveFile
from openCSV import writeToCSV
from openCSV import closeCSV


########################################################################
# ----- Constants ----- #
shouldWriteToFile = True
shouldPrint = False


########################################################################
# ----- Setup ----- #

# set the command to read pressures from the gauge
readCmd = "@254PR4?;FF"

# find any MKS gauges attached to the computer, then open the port and return
# the serial port object. Returns an empty string if it encounters any errors
# opening the communication port to the gauge.
serPort = setupGuagePort()

# if the serial port did not open properly, then exit
if not serPort:
    exit()


########################################################################
# ----- Device Comm ----- #
if serPort.isOpen():

    try:
        # open the .csv file to write to and save the writer object
        csvObjs = openSaveFile()

        # read from gauge until keyboard interrupt
        while True:

            (errorSTR, guageData) = readGauge(serPort, readCmd, shouldPrint)

            if not guageData:
                print('Lost contact with guage.')
                exit()

            print(guageData, "Torr")

            if shouldWriteToFile:
                writeToCSV(guageData, csvObjs)  # write to file

    except KeyboardInterrupt:
        print("Exiting Reading Loop")

    # print any of the errors received from the guage
    if not errorSTR:
        print("Exited communication with no device error.")
    else:
        print("Exited communication loop with error message: ", errorSTR)

    # close serial port once the communication has stopped
    serPort.close()

    # close the .csv log file after exiting the guage loop
    closeCSV(csvObjs)

else:

    print("Cannot open serial port.")
