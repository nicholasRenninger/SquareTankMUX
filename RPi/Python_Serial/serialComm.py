#!/usr/bin/env python3

"""
Enables serial communication with all devices defined in
'devices_settings.yaml'. Logs measurements to files in directory defined in
'logging_settings.yaml'.

Auto-detects and configures all settings associated with each device in the
settings file, returns a list of the configured device objects, and allows for
easy, configurable measurement of each device.
"""


########################################################################
# ----- Imports ----- #

from __future__ import print_function
from sys import exit
from deviceReadWrapper import readDevices
from setup import setupDevices
import openCSV
from OS_Calls import clear_screen


########################################################################
# ----- Author Info ----- #

__author__ = "Nicholas Renninger"
__copyright__ = "'Copyright' 2018, LASP"
__credits__ = ["Liam O'Swagger"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Renninger"
__email__ = "nicholas.renninger@colorado.edu"
__status__ = "Development"


########################################################################
# ----- Constants ----- #

SHOULD_WRITE_TO_FILE = True
SHOULD_PRINT = False
deviceSettingsFile = 'settings_files/devices_settings.yaml'
loggingSettingsFile = 'settings_files/logging_settings.yaml'


########################################################################
# ----- Setup ----- #

# get rid of any extra shit in shell stdout
clear_screen()

# Get a list of device measurements from CONNECTED, valid devices defined
# in the settings YAML file
deviceList = setupDevices(deviceSettingsFile)

fileSettings = openCSV.readInSettings(loggingSettingsFile)

########################################################################
# ----- Device Comm ----- #

try:
    # open the .csv file to write to and save the writer object
    csvObjs = openCSV.openSaveFile(fileSettings)

    # read from gauge until keyboard interrupt
    while True:

        measurements = readDevices(deviceList)

        if not measurements:
            print('Lost contact with devices.')
            exit()

        for idx, device in deviceList:
            print(device.name, ': ', measurements[idx],
                  ' [', device.meas_units, ']', sep='')

        if SHOULD_WRITE_TO_FILE:
            openCSV.writeToCSV(measurements, csvObjs, fileSettings)

except KeyboardInterrupt:
    print("Exiting Reading Loop")

# close serial port once the communication has stopped
for device in deviceList:
    device.ser_port.close()

# close the .csv log file after exiting the guage loop
openCSV.closeCSV(csvObjs)
