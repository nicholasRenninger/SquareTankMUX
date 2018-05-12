#!/usr/bin/env python3

from __future__ import print_function
import serial.tools.list_ports as portz
from initDevice import initializePort
from readSerialDevice import readDevice
from meas_device import meas_device

import yaml


# create list of valid Device Types from text file
with open('settings.txt', 'r') as f:
    DEVICE_INFO = readInSettings(f)

# initializations
WAIT_TIME = 1
shouldPrint = True
validPortList = []


def setupPort():
    """
    Returns the valid MUX serial port, and a list of addresses
    at the MUX that are connected to valid Devices.

    Note: The list of valid devices is given by a text file,
    'validDevicesList.txt', which contains the white-listed S/Ns of devices to
    be used.
    """

    # Find Live Ports
    ports = list(portz.comports())

    if not ports:
        print('No devices detected. Check connections / serial port,'
              'settings and try again.')
        return ""

    else:
        # Loop through all of the availible ports to determine if there are any
        # devices online.
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

            # If opening the connection was successful, determine if the port
            # is the port with MUX hardware.
            isMUXPort(serPort)
            (errorSTR, gaugeData) = readDevice(serPort, pressCMD, shouldPrint,
                                               WAIT_TIME)
            print(gaugeData, VALID_DEVICES)

            # now check if the device sends a valid device type back
            if gaugeData in VALID_DEVICES:
                print('Found', p.device)
                validPortList.append(serPort)

        if not validPortList:
            return validPortList
        else:
            # if no valid devices are found in the entire list, then print an
            # error
            print ('Did not find valid MKS gauge attached.',
                   'Check connections and try again.')

        return ""


def isMUXPort(serPort):
    """
    Returns true if the serial port, serPort, is the port connected
    to the MUX hardware.

    Note: The list of valid devices is given by a text file,
    'validDevicesList.txt', which contains the white-listed S/Ns of devices to
    be used.
    """


def readInSettings(file):
    """
    Returns list of meas_device objects for each
    device defined in 'settings.yaml':

    :param file: file object containing the settings lists
    :type file: open file object

    :returns: list of meas_device objects
    :rtype: list(meas_device)
    """

    # Read YAML file
    with open("settings.yaml", 'r', encoding='utf8') as stream:
        settings = yaml.load(stream)

    device_list = []
    for i in range(0, len(settings['NUM_DEVICES'])):

        # extract data for each device, and initlize device objects with this
        # data
        name = settings['DEVICES_TYPES'][i]
        idn_cmd = settings['IDN_CMD'][i]
        read_cmd = settings['READ_CMD'][i]
        idn_ack = settings['IDN_ACK'][i]
        is_muxed = settings['IS_MUXED'][i]
        ser_port = None
        mux_address = None
        err_nak = settings['ERR_NAK'][i]
        err_codes = settings['ERR_CODES'][i]

        newDevice = meas_device(name, idn_cmd, read_cmd, idn_ack, is_muxed,
                                ser_port, mux_address, err_nak, err_codes)
        device_list.append(newDevice)

    return device_list
