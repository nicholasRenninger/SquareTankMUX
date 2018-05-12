# SquareTankMUX - Python Serial Logging Application
This repo represents a vairety of experimentation with Ubuntu/Windows/Raspbian versions of python/C serial communication applications and Rapberry Pi serial MUXing for the purposes of automatic measurement of sensors attached to a clean-room vacuum chamber. 

The final application will identify all defined devices attached to any serial ports of a raspberry pi, including those connected to a multiplexed serial connection, and then allow for continuous reading of these devices over serial. All measurements taken will be recorded after every poll to a log file.

## Setup
To setup which devices are considered by the program, you must define each device in `*/Serial Logging/settings_files/device_settings.yaml`, filling out each field with the parameters of each device. If a parameter is a list, then the ith entry of the parameter corresponds to the ith device defined. All serial devices must use 9600-N-8-1 serial settings for the time being.

To setup the automatic logging of measurements, set the desired settings in `*/Serial Logging/settings_files/logging_settings.yaml`. Please ensure that that the `*/Logs` directory is at the relative path defined in this settings file, or the code will not know where to save files.

## Hardware Considerations
This project requires that a raspberry pi 3 is used, as the serial multiplexing relies on the GPIO pins being used for addressing.

The project was designed to use some custom PCBs fabricated to handle serial multiplexing (schematics found in the ECAD directory), but the program is flexible enough that it can still run on any device connected to a valid serial port on the raspberry pi. If you do not want to use this sort of serial multiplexing scheme, simply disable the multiplexing option for each device defined in `*/Serial Logging/settings_files/logging_settings.yaml`.

## Running the Code
The final application is contained in the `Serial Logging Application` directory, and it consists of only python files. To run the application, you will need to use Python 3.6 or later. The project has the following python3.6 module dependencies:

- pyyaml
- pySerial
- csv
- datetime
- logging modules

To run the code, ensure that you have the directory structure cloned properly, and that the `*/Logs` directory is at the relative path defined in the `*/Serial Logging/settings_files/logging_settings.yaml`. 

Then to run the program, simply type `python3.6 serialComm.py`.
