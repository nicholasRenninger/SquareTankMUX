#!/usr/bin/env python

# imports
import serial.tools.list_ports as portz
from initDevice import initializePort
from readMKSGauge import readGauge

# set the command to request device type data from gauge
deviceType = "@254DT?;FF"

# valid Device Types
VALID_DEVICES = ("MICROPIRANI", "DUALMAG")

# initializations
comport = "0"
comportIDX = 0


def setupGuagePort():

    # Find Live Ports
    ports = list(portz.comports())

    if not ports:
        print('No gauges detected. Check connections and try again.')
        return ""

    else:
        # Loop through all of the availible ports to determine if there are any
        # MKS gauges online.
        for p in ports:

            # open the port with the correct settings for an MKS gauge, and
            # with the current COM port being tested.
            serPort = initializePort(p.device)

            # open each valid port and see if the device is an MKS gauge
            # opening serial port
            try:
                serPort.open()

            except Exception as e:

                print("error opening serial port: ", str(e))
                return ""

            # If opening the gauge was successful, determine if the port is an
            # MKS gauge. If it is, return the serial port object.
            shouldPrint = True
            (errorSTR, guageData) = readGauge(serPort, deviceType, shouldPrint)

            if guageData in VALID_DEVICES:
                print('Using', p.device)
                return serPort
            else:
                print('Did not find valid MKS gauge attached.',
                      'Check connections and try again.')
                return ""
