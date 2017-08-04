#!/usr/bin/env python

import csv
import datetime
from collections import namedtuple


########################################################################
# opens a .csv file with write permissions and writes the headers
def openSaveFile():

    # auto-generate timestamp based filename
    curr_time = datetime.datetime.now()
    filename = 'pressure-log_' + curr_time.strftime("%Y%m%d-%H%M%S") + '.csv'

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
