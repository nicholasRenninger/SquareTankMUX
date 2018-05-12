#!/usr/bin/env python3.6

from __future__ import print_function
from sys import exit
import csv
import datetime
import os
from collections import namedtuple
import yaml


def readInSettings(settingsFile):
    """
    readInSettings(settingsFile)
    Returns dictionary of logging settings defined in YAML settings file,
    settingsFile.

    :param settingsFile: settingsFile object containing the settings lists
    :type settingsFile: open settingsFile object

    :returns: settings dictionary from settings file
    :rtype: dictionary
    """

    with open(settingsFile, 'r', encoding='utf8') as stream:
        settings = yaml.load(stream)

    return settings


########################################################################
# opens a .csv file with write permissions and writes the headers
def openSaveFile(settings):

    # set the relative path from the calling directory, base filename, and
    # file ext.
    base_path = os.path.dirname(os.path.realpath(__file__))

    rel_path = os.path.join(base_path, settings['rel_data_path'])

    file_ext = '.csv'

    # auto-generate timestamp based filename
    curr_time = datetime.datetime.now().strftime(settings['datetime_format'])
    filename = os.path.join(rel_path, settings['base_file_name'] +
                            curr_time + file_ext)

    try:
        csvfile = open(filename, 'w+')

    except Exception as error:

        print("error opening csv log file %s: " % filename, str(error))
        exit()

    fieldnames = settings['fieldnames']
    writer = csv.DictWriter(csvfile,
                            fieldnames=fieldnames,
                            lineterminator='\n')

    writer.writeheader()

    retObj = namedtuple('csvRetObjs', ['writer', 'csvfile'])
    csvObjs = retObj(writer, csvfile)

    return csvObjs


########################################################################
# takes the writer obj and writes the current measurements, along with the
# timestamp
def writeToCSV(measurements, csvObjs, settings):

    time_data = datetime.datetime.now()
    writeData = [float(i) for i in measurements]
    writeData.insert(0, time_data)

    headers = settings['fieldnames']
    writer = csvObjs.writer

    writer.writerow(dict(zip(headers, writeData)))
    csvObjs.csvfile.flush()


########################################################################
# close the .csv file used for logging
def closeCSV(csvObjs):

    csvObjs.csvfile.close()
