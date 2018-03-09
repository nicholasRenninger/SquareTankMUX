#!/usr/bin/env python3

# imports
from __future__ import print_function
import serial.tools.list_ports as portz
from initDevice import initializePort
from readMKSGauge import readGauge

# # set the command to request device type data from gauge
# pressCMD = "@254DT?;FF"

# set the command to request serial number from gauge
pressCMD = "@254SN?;FF"

# create list of valid Device Types from text file
with open('validDevicesList.txt', 'r') as f:

    VALID_DEVICES = f.readlines()

# initializations
comport = "0"
comportIDX = 0
rate = 1
validPortList = []


def setupGuagePort():

    """Returns list of valid device serial ports.

    Note: The list of valid devices is given by a text file,
    'validDevicesList.txt', which contains the white-listed S/Ns of devices to
    be used.
    """

    # Find Live Ports
    ports = list(portz.comports())

    if not ports:
        print('No gauges detected. Check connections and try again.')
        return ""

    else:
        # Loop through all of the availible ports to determine if there are any
        # MKS gauges online.
        for p in ports:

            print(p)

            # open the port with the correct settings for an MKS gauge, and
            # with the current COM port being tested.
            serPort = initializePort(p.device)

            # open each valid port and see if the device is an MKS gauge
            # opening serial port
            try:
                serPort.open()

            except Exception as e:

                print("error opening serial port: ", str(e))

            # If opening the gauge was successful, determine if the port is an
            # MKS gauge. If it is, return the serial port object.
            shouldPrint = True
            (errorSTR, guageData) = readGauge(serPort, pressCMD, shouldPrint,
                                              rate)
            print(guageData)

            # now check if the device sends a valid device type back
            if guageData in VALID_DEVICES:
                print('Using', p.device)
                validPortList.append(serPort)

        if not validPortList:
            return validPortList
        else:
            # if no valid devices are found in the entire list, then print an
            # error
            print ('Did not find valid MKS gauge attached.',
                   'Check connections and try again.')

        return ""
