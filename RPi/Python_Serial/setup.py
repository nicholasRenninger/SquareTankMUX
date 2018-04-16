#!/usr/bin/env python3

from __future__ import print_function

import serial.tools.list_ports as portz
from initDevice import initializePort
from meas_device import meas_device

import yaml
import RPi.GPIO as GPIO


def setupDevices(deviceSettingsFile):
    """
    setupDevices()
    Defines a list of possible valid devices which are configured from a YAML
    settings file. Then, sets up the serial ports associated with all of the
    devices that are connected to the computer that match the devices in the
    configuration file. Returns a list of these valid device objects with all
    of their necessary configuration

    :param deviceSettingsFile: the device settings file is given by this YAML
                               file in the working directory which contains
                               all of the device and hardware configuration
                               settings.
    :type deviceSettingsFile: (path) string
    """

    # create list of device objects configured with settings from settings file
    deviceObj_list = readInSettings(deviceSettingsFile)

    shouldPrint = True
    connectedDevices = []

    # Find Live Ports
    ports = list(portz.comports())

    if not ports:
        print('No devices detected. Check connections / serial port'
              ' settings and try again.')
        return None

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

            # If opening the connection was successful, determine what device
            # connected to serPort / MUX address
            for currDevice in deviceObj_list:

                currDevice.setPort(serPort)

                # if the returned currDevice ID string is the same as the
                # currDevice's idn_ack string, the device on serPort /
                # mux_address is really the valid device currDevice
                if currDevice.is_muxed:

                    # have to try all of the MUX ports
                    for mux_address in range(0, currDevice.numMuxAddresses):

                        currDevice.changeMUXStatus(mux_address)
                        idn_string = currDevice.read(shouldPrint, WAIT_TIME)

                        # need to remove currDevice from considered list of
                        # devices as there can only be one device with a
                        # certain type
                        if idn_string == currDevice.idn_ack:
                            connectedDevices.append(currDevice)
                            deviceObj_list.remove(currDevice)
                            break
                else:
                    idn_string = currDevice.read(shouldPrint, WAIT_TIME)

                    # need to remove currDevice from considered list of devices
                    # as there can only be one device with a certain type
                    if idn_string == currDevice.idn_ack:
                        connectedDevices.append(currDevice)
                        deviceObj_list.remove(currDevice)
                        break

        if not connectedDevices:
            return connectedDevices
        else:
            # if no valid devices are found in the entire list, then print an
            # error
            print('Did not find any valid measurement devices attached.',
                  'Check connections and try again.')

        return None


def readInSettings(settingsFile):
    """
    readInSettings(settingsFile)
    Returns tuple of:
    - list of meas_device objects for each evice defined in YAML
      settings file, settingsFile
    - the number of mux addresses

    :param settingsFile: settingsFile object containing the settings lists
    :type settingsFile: open settingsFile object

    :returns: list of meas_device objects with settings configured from the
              settings settingsFile
    :rtype: list(meas_device)
    """

    # Read YAML settings file
    with open(settingsFile, 'r', encoding='utf8') as stream:
        settings = yaml.load(stream)

    numMuxAddresses = settings['NUM_MUX_ADDRESSES']
    update_rate = settings['UPDATE_RATE']

    device_list = []
    for i in range(0, settings['NUM_DEVICES']):

        # extract data for each device, and initlize device objects with this
        # data
        name = settings['DEVICES_TYPES'][i]
        idn_cmd = settings['IDN_CMD'][i]
        read_cmd = settings['READ_CMD'][i]
        idn_ack = settings['IDN_ACK'][i]
        is_muxed = settings['IS_MUXED'][i]
        err_nak = settings['ERR_NAK'][i]
        err_codes = settings['ERR_CODES'][i]
        term_char = settings['DEVICE_TERM_CHARS'][i]
        num_start_chars = settings['DEVICE_TERM_CHARS'][i]
        meas_units = settings['MEAS_UNITS'][i]
        wait_time = settings['WAIT_TIME'][i]

        MUX_pins = [settings['MUX_ADDRESS_PIN_BIT_0'],
                    settings['MUX_ADDRESS_PIN_BIT_1'],
                    settings['MUX_ADDRESS_PIN_BIT_2']]
        inv_pin = settings['INVALID_PIN']
        forceOff_pin = settings['FORCE_OFF_PIN']

        ser_port = None
        mux_address = None

        newDevice = meas_device(name, idn_cmd, read_cmd, idn_ack, is_muxed,
                                ser_port, mux_address, err_nak, err_codes,
                                MUX_pins, inv_pin, forceOff_pin, term_char,
                                num_start_chars, meas_units, numMuxAddresses,
                                update_rate, wait_time)
        device_list.append(newDevice)

    GPIO_out_pins = MUX_pins
    GPIO_in_pins = [inv_pin, forceOff_pin]
    setGPIOPins(GPIO_out_pins, GPIO_in_pins)

    return device_list


def setGPIOPins(GPIO_out_pins, GPIO_in_pins):
    """
    setGPIOPins(pinsToSet)
    sets all of the GPIO pins in the list pinsToSet on the RPi to be in digital
    output mode (LOW-Z)

    :param GPIO_out_pins: list of GPIO pins to set as GPIO OUT
    :type GPIO_out_pins: list(int)
    :param GPIO_in_pins: list of GPIO pins to set as GPIO IN
    :type GPIO_in_pins: list(int)
    """

    # Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # setup all of the pins to be digital in / out
    for GPIO_Pin in GPIO_out_pins:
        GPIO.setup(GPIO_Pin, GPIO.OUT)

    for GPIO_Pin in GPIO_in_pins:
        GPIO.setup(GPIO_Pin, GPIO.IN)
