#!/usr/bin/env python

from __future__ import print_function
import csv
import datetime
import os
from collections import namedtuple


########################################################################
# opens a .csv file with write permissions and writes the headers
def openSaveFile():

    # set the relative path from the calling directory, base filename, and
    # file ext.
    base_path = os.path.dirname(os.path.realpath(__file__))
    rel_folder_path = "Logs"
    rel_path = os.path.join(base_path, rel_folder_path)

    file_ext = '.csv'
    base_file_name = 'pressure-log_'

    # auto-generate timestamp based filename
    curr_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(rel_path, base_file_name + curr_time + file_ext)

    try:
        csvfile = open(filename, 'w+')

    except Exception as error:

        print("error opening serial port: ", str(error))
        exit()

    fieldnames = ['Timestamp', 'Pressure [torr]']
    writer = csv.DictWriter(csvfile,
                            fieldnames=fieldnames,
                            lineterminator='\n')

    writer.writeheader()

    retObj = namedtuple('csvRetObjs', ['writer', 'csvfile'])
    csvObjs = retObj(writer, csvfile)

    return csvObjs


########################################################################
# takes the writer obj and writes the current pressure, along with the
# timestamp
def writeToCSV(pressure, csvObjs):

    time_data = datetime.datetime.now()

    writer = csvObjs.writer
    writer.writerow({'Timestamp': time_data, 'Pressure [torr]': pressure})


########################################################################
# close the .csv file used for logging
def closeCSV(csvObjs):

    csvObjs.csvfile.close()
