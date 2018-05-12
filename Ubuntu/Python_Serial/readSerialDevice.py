# imports
from __future__ import print_function
import time

# codes in guage return strings which indicate device status
ERROR_MARKER = "NAK"
OK_MARKER = "ACK"

# possible error codes for MKS gauges
MKS_ERROR_DICT = {"8": "Zero adjustment at too high pressure",
                  "9": "Atmospheric adjustment at too low pressure",
                  "160": "Unrecognized message",
                  "169": "Invalid argument",
                  "172": "Value out of range",
                  "175": "Command/query character invalid",
                  "180": "Not in setup mode (locked)"}


def readDevice(serPort, readCommand, shouldPrint, WAIT_TIME):
    """
    Returns data from the device at serPort's output buffer.

    serPort: an instance of the Serial Port Class, connected to a valid, open
             device

    readCommand: a string containing the command to be sent over serial to the
                 device

    shouldPrint: boolean flag as to whether you should print the data received
                 from the device to stdout

    WAIT_TIME: amount of time for the serial port to sleep between the request
               for data and reading from the device's output buffer.
               [s]

    """

    # flush input buffer, discarding all its contents
    serPort.flushInput()

    # flush output buffer, aborting current output and discard all that is
    # in buffer
    serPort.flushOutput()

    # write data
    serPort.write(readCommand.encode('ascii'))

    # give the serial port some time to receive the data
    time.sleep(WAIT_TIME)

    # this will store the line read from the gauge
    currLine = serPort.readline().decode("utf-8")

    # remove addressing and termination from data
    data = currLine[7:]  # get rid of everything before error message
    data = data[:-3]  # cut off termination

    # checking for known error codes in the return string from the gauge
    if ERROR_MARKER in currLine:

        if data in MKS_ERROR_DICT:
            errorSTR = "error #", data, ":", MKS_ERROR_DICT[data]
        else:
            errorSTR = "error #", data, " not recognized."

    else:  # no error
        errorSTR = ""

    if shouldPrint:
        print('write data: ', readCommand)

        if not data:
            print('No response from', serPort.port, '\n')
        else:
            print('Connected to', data, 'guage\n')

    return (errorSTR, data)
