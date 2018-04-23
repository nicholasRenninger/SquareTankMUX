#!/usr/bin/env python3

from __future__ import print_function
from time import time


def readDevices(deviceList):
    """
    Returns a list of device measurements from CONNECTED, valid devices defined
    in the settings YAML file. Reads each device sequentially, with the
    measurement of each device completed every deviceList[0].update_rate [s]

    :param deviceList: list of valid, connected meas_device objects to be
                       measured
    :type deviceList: list(meas_device)
    """

    print(deviceList[0])

    # need to calculate how long each guage can wait to be read to ensure the
    # total delay is equal to deviceList[0].update_rate.
    POLL_RATE = deviceList[0].update_rate / len(deviceList)

    measList = []
    start = time()
    shouldPrint = False

    # this loop should take about deviceList[0].update_rate [s] to run
    for device in deviceList:
        measurement = device.read(shouldPrint, POLL_RATE)
        measList.append(measurement)

    end = time()
    print('Took', end - start, '[s] to read all', len(deviceList),
          'connected devices')
    return measList
