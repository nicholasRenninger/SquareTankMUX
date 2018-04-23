#!/usr/bin/env python3

from __future__ import print_function
import time
import RPi.GPIO as GPIO
import math
import logging


class meas_device:

    def __init__(self, dev_name, idn_cmd, read_cmd, idn_ack, is_muxed,
                 ser_port, MUX_address, err_nak, err_codes, MUX_pins,
                 inv_pin, forceOff_pin, term_char, num_start_chars,
                 meas_units, numMuxAddresses, update_rate, wait_time):
        """
        self.__init__(self, dev_name, idn_cmd, read_cmd, idn_ack, is_muxed,
                      ser_port, MUX_address, err_nak, err_codes, MUX_pins,
                      inv_pin, forceOff_pin, term_char, num_start_chars,
                      meas_units, numMuxAddresses, update_rate)

        Initializes an instance of a measurement device object, which has
        fields defined below:

        :param dev_name: string with the display name of the device
        :type dev_name: str
        :param idn_cmd: string containing full string sent to device over
                        serial for IDN command - MUST HAVE TERMINATION CHAR
        :type idn_cmd: str
        :param read_cmd: string containing full string sent to device over
                        serial for READ command - MUST HAVE TERMINATION CHAR
        :type read_cmd: str
        :param idn_ack: string containing full string you expect to receive
                        over serial after IDN command
        :type idn_ack: str
        :param is_muxed: boolean value determining whether the device is
                         connected to a multiplexed serial port or not
        :type is_muxed: bool
        :param ser_port: serial port object that the device is connected
                         over
        :type ser_port: serial port object
        :param MUX_address: address used in the serial MUX to identify the
                            device. is None if the device is not muxed
        :type MUX_address: int
        :param err_nak: string device will use to identify its data as an
                        error code
        :type err_nak: bool
        :param err_codes: boolean value determining whether the device is
                         connected to a multiplexed serial port or not
        :type err_codes: bool
        :param MUX_pins: list of GPIO pins used for MUX_address. List is in
                         little-endian form (LSB to MSB)
        :type MUX_pins: list(ints)
        :param inv_pin: GPIO pin corresponding to the invalid state outputted
                        by the MUX board. if this pin is low (0), then
                        nothing is connected to current MUX address
                        set on the MUX board
        :type inv_pin: int
        :param forceOff_pin: GPIO pin corresponding to the forceOff state
                             outputted by the MUX board. if this pin is low
                             (0), board is in a bad state (voltages, etc.) -
                            print error and halt
        :type forceOff_pin: int
        :param term_char: string with the serial termination character used by
                          the device
        :type term_char: string
        :param num_start_chars: number of characters to strip from raw output
                                serial read of device to record a measurement
        :type num_start_chars: int
        :param meas_units: units of any measurement from the device
        :type meas_units: string
        :param numMuxAddresses: max. num. of addresses supported by MUX board
        :type numMuxAddresses: int
        :param update_rate: how often the device will be measured
        :type update_rate: float [s]
        :param wait_time: time to wait from device querry to device read
        :type wait_time: float [s]

        :returns: initialized meas_device object
        :rtype: meas_device object
        """

        self.name = dev_name
        self.idn_cmd = idn_cmd
        self.read_cmd = read_cmd
        self.idn_ack = idn_ack
        self.is_muxed = is_muxed
        self.ser_port = None
        self.MUX_address = None
        self.err_nak = err_nak
        self.err_codes = err_codes
        self.MUX_pins = MUX_pins
        self.inv_pin = inv_pin
        self.forceOff_pin = forceOff_pin
        self.term_char = term_char
        self.num_start_chars = num_start_chars
        self.meas_units = meas_units
        self.numMuxAddresses = numMuxAddresses
        self.update_rate = update_rate
        self.wait_time = wait_time

    def setPort(self, newPort):
        """
        setPort(self, newPort)
        Updates the ser_port attribute of the device object with the serial
        port at newPort.

        :param newPort: should be the serial port contained in self.ser_port
                        after this method is run
        :type newPort: serial port object
        """

        self.ser_port = newPort

    def setMUXAddress(self, newAddress):
        """
        setMUXAddress(self, newAddress)
        Updates the MUX_address attribute of the device object with the address
        newAddress.

        :param newAddress: should be the mux address contained in
                           self.newAddress after this method is run
        :type newAddress: serial port object
        """

        self.MUX_address = newAddress

    def data2Measurement(self, raw_data):
        """
        data2Measurement(raw_data)
        Converts raw data string into a measurement of the same units as is
        defined by self.meas_units

        :param raw_data: raw string received from a serial read of the device's
                         output buffer
        :type raw_data: string

        :returns: measurement converted from data string with units defined by
                  self.meas_units
        :rtype: string (UTF-8)
        """
        print(self.num_start_chars)

        # remove addressing and termination from data
        data = raw_data[self.num_start_chars:]

        # cut off termination
        data = data[:-(len(self.term_char))]

        return data

    def setMUXAddressPins(self):
        """
        setMUXAddressPins(self)
        Sets GPIO MUX address pins for serial read
        """

        numAddressBits = int(math.ceil(math.log(self.numMuxAddresses) /
                                       math.log(2)))

        # address will be a binary string, which will be sent to the GPIO
        # pins succesively. don't take the 0b portion of 0b101...
        LEDAddress = '%0*d' % (numAddressBits,
                               int(bin(self.MUX_address)[2:]))

        # write MUX address to the GPIO pins
        for idx, currentPin in enumerate(LEDAddress):

            print('current pin = ', currentPin)

            # Setup the MUX
            if (currentPin == '1'):
                GPIO.output(self.MUX_pins[idx], GPIO.HIGH)
                print(self.MUX_pins[idx], 'is high')
            else:
                # currentPin = 0
                print(self.MUX_pins[idx], 'is low')
                GPIO.output(self.MUX_pins[idx], GPIO.LOW)

    def idn_read(self, WAIT_TIME):
        """
        self.idn_read(self, WAIT_TIME)
        Error Wrapper (public method) for the self.__read__() method, which
        querries the device with its idn_cmd

        :param WAIT_TIME: amount of time for the serial port to sleep
                          between the request for data and reading from
                          the device's output buffer.
                          [s]
        :type WAIT_TIME: float

        :returns: raw data string from device serial read buffer
        :rtype: string (UTF-8)
        """

        logger = logging.getLogger(__name__)

        shouldPrint = True
        isIDN = True
        
        try:
            data = self.__read__(shouldPrint, WAIT_TIME, isIDN)
        except ValueError as e:
            logger.error(e)
            raise

        return data

    def read(self, shouldPrint, WAIT_TIME):
        """
        self.read(self, shouldPrint, WAIT_TIME)
        Error Wrapper (public method) for the self.__read__() method.

        :param shouldPrint: boolean flag as to whether you should print the
                            data received from the device to stdout
        :type shouldPrint: bool
        :param WAIT_TIME: amount of time for the serial port to sleep
                          between the request for data and reading from
                          the device's output buffer.
                          [s]
        :type WAIT_TIME: float

        :returns: raw data string from device serial read buffer
        :rtype: string (UTF-8)
        """

        logger = logging.getLogger(__name__)
        
        shouldPrint = False
        isIDN = False

        try:
            data = self.__read__(shouldPrint, WAIT_TIME, isIDN)
        except ValueError as e:
            logger.error(e)
            raise

        return data

    def __read__(self, shouldPrint, WAIT_TIME, isIDN):
        """
        self.read(self, shouldPrint, WAIT_TIME)
        Returns string data from the device at ser_port's output buffer.

        :param shouldPrint: boolean flag as to whether you should print the
                            data received from the device to stdout
        :type shouldPrint: bool
        :param WAIT_TIME: amount of time for the serial port to sleep
                          between the request for data and reading from
                          the device's output buffer.
                          [s]
        :type WAIT_TIME: float
        :param isIDN: boolean flag to tell read to only use idn_cmd
        :type isIDN: bool

        :returns: raw data string from device serial read buffer
        :rtype: string (UTF-8)
        """

        # flush input buffer, discarding all its contents
        self.ser_port.flushInput()

        # flush output buffer, aborting current output and discard all that is
        # in buffer
        self.ser_port.flushOutput()

        # write data
        if isIDN:
            write_cmd = self.idn_cmd
        else:
            write_cmd = self.read_cmd

        self.ser_port.write(write_cmd.encode('ascii'))

        # give the serial port some time to receive the data
        time.sleep(WAIT_TIME)

        # self.inv_pin is low when there is no device on the current
        # MUX_address
        if self.is_muxed:
            if GPIO.input(self.inv_pin):
                self.setMUXAddressPins()
            else:
                return None

        # reads buffer of guage and formats and converts raw data to a
        # measurement value with the units of self.meas_units
        currLine = self.ser_port.readline().decode('utf-8')

        if isIDN:
            data = self.data2Measurement(currLine)
        else:
            data = self.data2Measurement(currLine)

        # checking for known error codes in the return string from the gauge
        if self.err_nak in currLine:

            if data in self.err_codes:
                errorSTR = 'error #', data, ':', self.err_codes[data]
            elif GPIO.input(self.forceOff_pin):
                errorSTR = 'Force-on pin on MUX board is active: check' \
                           ' MUX board / connected devices for electrical' \
                           ' malfunction'
            else:
                errorSTR = 'error #', data, ' not recognized'

            raise ValueError('Error Reading from Device: {}', errorSTR)

        if shouldPrint:
            print('write data: ', self.read_cmd)

            if not data:
                print('No response from', self.ser_port.port, '\n')
            else:
                print('Connected to', data, 'guage\n')

        return data
