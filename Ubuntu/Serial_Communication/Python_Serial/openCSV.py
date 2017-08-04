#!/usr/bin/env python3

import csv
import datetime


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

    return writer


########################################################################
# takes the writer obj and writes the current pressure, along with the
# timestamp
def writeToCSV(pressure, writer):

    time_data = datetime.datetime.now()
    writer.writerow({'Timestamp': time_data, 'Pressure [torr]': pressure})
