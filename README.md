Elcometer456
============

This block will read from an Elcometer digital zinc mil gage via virtual serial
connection.

If the device is not paired with the n.io host, then the block will retry
connecting every 10 seconds until the bluetooth device is paired.

Properties
--------------

-   port (type=str): Serial port to read from
-   baudrate (type=int): Baud rate of serial port

Dependencies
----------------

-   [pyserial](https://pypi.python.org/pypi/pyserial)

Commands
----------------
None

Input
-------
Reading from digital zinc gage

Ex:  b'   3.14 mil  N1    \r\n'

Output
---------
A signal containing the output reading of the gage (float) in mils. If `---` is
read no signals are notified.
