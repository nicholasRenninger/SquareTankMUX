class meas_device:

    # TODO: implement read(), addPort(), addMUXAddress() methods

    def __init__(self, dev_name, idn_cmd, read_cmd, idn_ack, is_muxed,
                 ser_port, MUX_address, err_nak, err_codes):
        """
        meas_device.__init__(idn_cmd, read_cmd, idn_ack):
        creates an instance of a measurement device object, which has fields
        defined below.

        :param dev_name: string with the display name of the device
        :type dev_name: str
        :param idn_cmd: string containing full string sent to device over
                        serial for IDN command - MUST HAVE TERMINATION CHAR
        :type idn_cmd: str
        :param read_cmd: string containing full string sent to device over
                        serial for READ command - MUST HAVE TERMINATION CHAR
        :type read_cmd: str
        :param idn_ack: string containing full string you expect to receive
                        over serial after IDN command
        :type idn_ack: str
        :param is_muxed: boolean value determining whether the device is
                         connected to a multiplexed serial port or not
        :type is_muxed: bool
        :param ser_port: serial port object that the device is connected
                         over
        :type ser_port: serial port object
        :param MUX_address: address used in the serial MUX to identify the
                            device. is None if the device is not muxed
        :type MUX_address: int
        :param err_nak: string device will use to identify its data as an
                        error code
        :type err_nak: bool
        :param err_codes: boolean value determining whether the device is
                         connected to a multiplexed serial port or not
        :type err_codes: bool

        :returns: initialized meas_device object
        :rtype: meas_device object
        """

        self.name = dev_name
        self.idn_cmd = idn_cmd
        self.read_cmd = read_cmd
        self.idn_ack = idn_ack
        self.is_muxed = is_muxed
        self.ser_port = None
        self.MUX_address = None
        self.err_nak = err_nak
        self.err_codes = err_codes
