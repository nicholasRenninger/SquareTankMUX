#!/usr/bin/env python3.6

from __future__ import print_function
from time import time


def readDevices(connectedDevices, allPossibleDevices):
    """
    readDevices(connectedDevices, allPossibleDevices)
    Returns a list of device measurements from CONNECTED, valid devices defined
    in the settings YAML file. Reads each device sequentially, with the
    measurement of each device completed every
    connectedDevices[0].update_rate [s]

    :param connectedDevices: list of valid, connected meas_device objects to be
                       measured
    :type connectedDevices: list(meas_device)
    :param allPossibleDevices: list of all possible devices defined in the
                               config file
    :type allPossibleDevices: list(meas_device)

    :returns: list of measurements taken for all possible devices defined. Any
              device not connected will have 'NaN' reported as its measurement
    :rtype: list(str)
    """

    # need to calculate how long each guage can wait to be read to ensure the
    # total delay is equal to connectedDevices[0].update_rate.
    POLL_RATE = connectedDevices[0].update_rate / len(connectedDevices)

    tempList = []
    start = time()
    shouldPrint = False

    # this loop should take about connectedDevices[0].update_rate [s] to run
    for device in connectedDevices:
        measurement = device.read(shouldPrint, POLL_RATE)
        tempList.append(measurement)

    # add NaN values for all un-connected devices
    measList = []
    for device in allPossibleDevices:
        if device in connectedDevices:
            idx = connectedDevices.index(device)
            measList.append(tempList[idx])
        else:
            measList.append('NaN')

    end = time()
    print('Took', end - start, '[s] to read all', len(connectedDevices),
          'connected devices')

    return measList
