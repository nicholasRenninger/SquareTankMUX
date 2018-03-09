#!/usr/bin/env python

# imports
import serial


def initializePort(portname):

    """Returns an instance of the Serial Port Class, connected to a valid, open
       device.

    portname: string containing the serial port name to read from.
    """

    # create serial port object
    serPort = serial.Serial()

    # setup the serial port with the passed portname e.g. COM5
    serPort.port = portname

    serPort.baudrate = 9600  # max bits per sec transf speed
    serPort.bytesize = serial.EIGHTBITS  # number of bits per bytes
    serPort.parity = serial.PARITY_NONE  # set parity check: no parity
    serPort.stopbits = serial.STOPBITS_ONE  # number of stop bits
    serPort.timeout = 0  # non-block read
    serPort.xonxoff = False  # disable software flow control
    serPort.rtscts = False  # disable hardware (RTS/CTS) flow control
    serPort.dsrdtr = False  # disable hardware (DSR/DTR) flow control
    serPort.writeTimeout = 0  # timeout for write

    return serPort
