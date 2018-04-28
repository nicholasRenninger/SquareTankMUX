#!/usr/bin/env python3.6

from __future__ import print_function

import serial.tools.list_ports as portz
from initDevice import initializePort
from meas_device import meas_device

import yaml
import RPi.GPIO as GPIO
import difflib


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

    :returns: tuple of lists of all possible devices and valid devices that
              have been found onserial ports, and have had their info updated.
              Returns (allPossibleDevices, None) if no valid devices are found.
    :rtype: tuple(list(meas_device), list(meas_device))
    """

    # create list of device objects configured with settings from settings file
    deviceObj_list = readInSettings(deviceSettingsFile)
    allPossibleDevices = deviceObj_list[:]

    connectedDevices = []

    # Find Live Ports
    ports = list(portz.comports())

    if not ports:
        print('No devices detected. Check connections / serial port'
              ' settings and try again.')
        return (allPossibleDevices, None)

    else:
        # Loop through all of the availible ports to determine if there are any
        # devices online.
        for p in ports:

            print('Trying connections to', p)

            # open the port with the correct settings for an MKS gauge, and
            # with the current COM port being tested.
            serPort = initializePort(p.device)

            # open each valid port and see if the device is an MKS gauge
            # opening serial port
            try:
                serPort.open()

            except Exception as e:

                print("error opening serial port: ", str(e))

            findDevicesOnPort(serPort, deviceObj_list, connectedDevices)

        print('\n\nConnected Devices:')
        for device in connectedDevices:
            print(device.name)
        print('\n')

        if connectedDevices:
            return (allPossibleDevices, connectedDevices)
        else:
            # if no valid devices are found in the entire list, then print an
            # error
            print('Did not find any valid measurement devices attached.',
                  'Check connections and try again.')

        return (allPossibleDevices, None)


def findDevicesOnPort(serPort, deviceObj_list, connectedDevices):
    """
    findDevicesOnPort(serPort, deviceObj_list, connectedDevices)
    Searches serPort for any devices in deviceObj_list that are valid, and if
    it finds a valid device connected, it removes that device from the list of
    devices to search (deviceObj_list), and adds this device and its updated
    port / MUX info to connectedDevices. Returns true if the function found any
    valid device attached to serPort

    :param serPort: the current serial port under consideration
    :type serPort: pySerial serial port instance
    :param deviceObj_list: list of devices still not found on any serial port
    :type deviceObj_list: list(meas_device)
    :param connectedDevices: list of valid devices that have been found on
                             serial ports, and have had their info updated
    :type connectedDevices: list(meas_device)

    :returns: whether or not any valid devices were found on the port,
              implicitly modifies deviceObj_list and connectedDevices by
              removing and adding devices (respectively) as they are found.
    :rtype: bool
    """

    # need to update deviceObj_list to remove devices that are found on this
    # port so they are not searched in the future, so create new copy here for
    # iteration, and update the orignal device list accordingly
    tempDevList = deviceObj_list[:]

    foundDevice = False

    # If opening the connection was successful, determine what device
    # connected to serPort / MUX address
    for currDevice in tempDevList:

        print('Attempting connection to', currDevice.name)
        currDevice.setPort(serPort)

        # if the returned currDevice ID string is the same as the
        # currDevice's idn_ack string, the device on serPort /
        # mux_address is really the valid device currDevice
        if currDevice.is_muxed:

            # have to try all of the MUX ports
            for mux_address in range(0, currDevice.numMuxAddresses):

                # if this is the right mux_address, then the
                # mux address will already be set
                print('Trying MUX address:', mux_address)
                currDevice.setMUXAddress(mux_address)
                idn_string = currDevice.idn_read(currDevice.wait_time)

                # need to remove currDevice from considered list of
                # devices as there can only be one device with a
                # certain type
                if idn_string == currDevice.idn_ack:
                    print('Connected to', currDevice.name, 'on',
                          currDevice.ser_port.port, 'with MUX Address',
                          currDevice.MUX_address, '\n')
                    connectedDevices.append(currDevice)
                    deviceObj_list.remove(currDevice)
                    foundDevice = True

                    # stop changing mux addresses once found
                    break
                else:
                    # not a valid device, be sure to set the
                    # device's mux address back to 'None' for safety
                    currDevice.setMUXAddress(None)

        else:
            idn_string = currDevice.idn_read(currDevice.wait_time)

            show_diff(idn_string, currDevice.idn_ack)

            # need to remove currDevice from considered list of devices
            # as there can only be one device with a certain type
            if idn_string == currDevice.idn_ack:
                print('Connected to', currDevice.name, 'on',
                      currDevice.ser_port.port, ' (not MUXed)')
                connectedDevices.append(currDevice)
                deviceObj_list.remove(currDevice)
                foundDevice = True

    return foundDevice


def show_diff(text, n_text):
    """
    http://stackoverflow.com/a/788780
    Unify operations between two compared strings seqm is a difflib.
    SequenceMatcher instance whose a & b are strings
    """
    seqm = difflib.SequenceMatcher(None, text, n_text)
    output = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append("<font color=red>^" + seqm.b[b0:b1] + "</font>")
        elif opcode == 'delete':
            output.append("<font color=blue>^" + seqm.a[a0:a1] + "</font>")
        elif opcode == 'replace':
            # seqm.a[a0:a1] -> seqm.b[b0:b1]
            output.append("<font color=green>^" + seqm.b[b0:b1] + "</font>")
        else:
            print('bad touch sir')
    return ''.join(output)


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
        num_start_chars = settings['DEVICE_DATA_START_CHARS'][i]
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
    print('Input Pins:', GPIO_out_pins)
    print('Output Pins:', GPIO_out_pins)
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
