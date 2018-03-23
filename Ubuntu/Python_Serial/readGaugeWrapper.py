# imports
from __future__ import print_function
from readMKSGauge import readGauge
from time import time


def readGauges(serPortList, readCommand, shouldPrint, UPDATE_RATE):
    """
    Returns a list of data read from the output buffer of all devices in
       serPortList. Returns an empty list if an error occurred.

    serPortList: a list of valid instances of the Serial Port Class, connected
                 to valid, open  devices.

    readCommand: a string containing the command to be sent over serial to the
                 device

    shouldPrint: boolean flag as to whether you should print the data received
                 from the device to stdout

    UPDATE_RATE: how long it should take to read from all guages and return
                 list of guage data.
                 [s]

    """

    # need to calculate how long each guage can wait to be read to ensure the
    # total delay is equal to UPDATE_RATE.
    UPDATE_RATE = 1 / len(serPortList)

    # initialize
    gaugeDataList = []

    start = time.time()

    # this loop should take about UPDATE_RATE to run
    for port in serPortList:

        try:

            (errorSTR, guageData) = readGauge(serPortList, readCommand,
                                              shouldPrint, UPDATE_RATE)

            # print any of the errors received from the guage
            if not errorSTR:
                print("Exited communication with no device error.")
            else:
                print("Exited communication loop with error message: ",
                      errorSTR)
                return ""

            gaugeDataList.append(guageData)

        except Exception as e:
            print("error reading from device: ", str(e))

    end = time.time()
    print(end - start)
    return gaugeDataList
