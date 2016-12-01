Elcometer456
============

This block will read from an Elcometer digital zinc mil gage via virtual serial connection
In its current state, this block assumes that the device is connected via 
bluetooth and will only start if a virtual serial port can be opened.


Properties
--------------

-   port (str): Serial port to read from
-   baudrate (int): Baud rate of serial port
-   timeout (int): Read timeout in seconds

Dependencies
----------------

-   [pyserial](https://pypi.python.org/pypi/pyserial)

Commands
----------------
None

Input
-------
Reading from digital zinc gage

Output
---------
A signal containing the output reading of the gage in bytes. 

-------------------------------------------------------------------------------

