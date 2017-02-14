import serial
from nio.signal.base import Signal
from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty, IntProperty
from nio.util.threading.spawn import spawn


class Elcometer456(Block):

    """ Read from an Elcometer digital bluetooth gage """

    version = VersionProperty('0.1.0')
    port = StringProperty(title='Port', default='COM7')
    baudrate = IntProperty(title='Baud Rate', default=9600)
    timeout = IntProperty(title='Timeout', default=100)

    def __init__(self):
        super().__init__()
        self._serial = None
        self._thread = None

    def configure(self, context):
        super().configure(context)
        self._serial = serial.Serial(self.port(), self.baudrate(), timeout=self.timeout())

    def start(self):
        super().start()
        self._thread = spawn(self._read_gage)

    def stop(self):
        self._serial.close()
        self._thread.join(1)
        super().stop()

    def _read_gage(self):
        self.logger.debug('Start reading')
        while self._serial.isOpen() == True:
            self.logger.debug('Waiting for reading')
            raw = self._serial.readline()
            self._serial.write(b"O")
            read = b''
            if str(raw).split()[1] != '---':
                read = float(str(raw).split()[1])
            self.notify_signals([Signal({'value': read})])
            self.logger.debug('Gage Reading: ' + str(read) + ' mils')
