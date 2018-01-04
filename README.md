Elcometer456
============

This block will read from an Elcometer digital zinc mil gage via virtual serial
connection.

If the device is not paired with the n.io host, then the block will retry
connecting every 10 seconds until the bluetooth device is paired.

Properties
----------
- **baudrate**: Baud rate of serial port.
- **port**: Serial port to read from.
- **timeout**: Timeout for reading from serial port.

Inputs
------
None

Outputs
-------
- **default**: A signal containing the output reading of the gage (float) in mils. If `---` is
 read no signals are notified.

Commands
--------
None

Dependencies
------------
-   [pyserial](https://pypi.python.org/pypi/pyserial)
