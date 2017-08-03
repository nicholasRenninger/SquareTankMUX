# imports
import time

# codes in guage return strings which indicate device status
ERROR_MARKER = "NAK"
GOOD_MARKER = "ACK"

# possible error codes for MKS gauges
ERROR_DICT = {"8": "Zero adjustment at too high pressure",
              "9": "Atmospheric adjustment at too low pressure",
              "160": "Unrecognized message",
              "169": "Invalid argument",
              "172": "Value out of range",
              "175": "Command/query character invalid",
              "180": "Not in setup mode (locked)"}


def readGauge(serPort, readCommand, shouldPrint):

    # flush input buffer, discarding all its contents
    serPort.flushInput()

    # flush output buffer, aborting current output and discard all that is
    # in buffer
    serPort.flushOutput()

    # write data
    serPort.write(readCommand.encode('ascii'))

    time.sleep(0.1)  # give the serial port some time to receive the data

    # this will store the line read from the gauge
    currLine = serPort.readline().decode("utf-8")

    # remove addressing and termination from data
    guageData = currLine[7:]  # get rid of everything before error message
    guageData = guageData[:-3]  # cut off termination

    # checking for known error codes in the return string from the gauge
    if ERROR_MARKER in currLine:

        if guageData in ERROR_DICT:
            errorSTR = "error #", guageData, ":", ERROR_DICT[guageData]
        else:
            errorSTR = "error #", guageData, " not recognized."

    else:  # no error
        errorSTR = ""

    if shouldPrint:
        print('write data: ', readCommand)
        print(guageData)

    return (errorSTR, guageData)
