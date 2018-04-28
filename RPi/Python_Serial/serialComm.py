#!/usr/bin/env python3.6

"""
Enables serial communication with all devices defined in
'devices_settings.yaml'. Logs measurements to files in directory defined in
'logging_settings.yaml'.

Auto-detects and configures all settings associated with each device in the
settings file, returns a list of the configured device objects, and allows for
easy, configurable measurement of each device.

Requires Python 3.6 to work properly, as well as the pyyaml, pySerial, and
openCSV.
"""
from __future__ import print_function

from deviceReadWrapper import readDevices
from OS_Calls import clear_screen
from setup import setupDevices

from sys import exit
import openCSV


########################################################################
# ----- Author Info ----- #

__author__ = "Nicholas Renninger"
__copyright__ = "'Copyright' 2018, LASP"
__credits__ = ["Liam O'Swagger"]
__license__ = "MIT"
__version__ = "1.3.0"
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

# Get a list of device objects from CONNECTED, valid devices defined
# in the settings YAML file
(allPossibleDevices, connectedDevices) = setupDevices(deviceSettingsFile)

if not connectedDevices:
    print('No Valid Devices Found. Ending Program.')
    exit()

fileSettings = openCSV.readInSettings(loggingSettingsFile)

########################################################################
# ----- Device Comm ----- #

try:
    # open the .csv file to write to and save the writer object
    csvObjs = openCSV.openSaveFile(fileSettings)

    # read from gauge until keyboard interrupt
    while True:

        measurements = readDevices(connectedDevices, allPossibleDevices)

        if not measurements:
            print('Lost contact with devices.')
            exit()

        for idx, device in enumerate(allPossibleDevices):
            print(device.name, ': ', measurements[idx],
                  ' [', device.meas_units, ']', sep='')
        print('\n')

        if SHOULD_WRITE_TO_FILE:
            openCSV.writeToCSV(measurements, csvObjs, fileSettings)

except KeyboardInterrupt:
    print("Exiting Reading Loop")

# close serial port once the communication has stopped
for device in connectedDevices:
    device.ser_port.close()

# close the .csv log file after exiting the guage loop
openCSV.closeCSV(csvObjs)
