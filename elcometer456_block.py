import serial
from time import sleep
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
        self._connect_thread = None
        self._read_thread = None
        self._stopping = False

    def start(self):
        super().start()
        self._connect_thread = spawn(self._connect_gage)

    def stop(self):
        self._stopping = True
        if self._connect_thread:
            self._connect_thread.join(1)
        if self._serial:
            self._serial.close()
        if self._read_thread:
            self._read_thread.join(1)
        super().stop()

    def _connect_gage(self):
        while True:
            if self._stopping:
                return
            try:
                self._serial = serial.Serial(self.port(), self.baudrate(), timeout=self.timeout())
                self.logger.info('Pairing Successful')
            except:
                self.logger.warning('Pairing attempt failed', exc_info = False)
                sleep(10)
                continue
            break
        self._read_thread = spawn(self._read_gage)

    def _read_gage(self):
        self.logger.debug('Start reading')
        while self._serial.isOpen() == True:
            if self._stopping:
                return
            self.logger.debug('Waiting for reading')
            try:
                raw = self._serial.readline()
            except serial.SerialException:
                if not self._stopping:
                    self.logger.info('Closing serial connection')
                    self._serial.close()
                continue
            self._serial.write(b"O")
            read = 0
            if str(raw).split()[1] != '---':
                read = float(str(raw).split()[1])
            self.notify_signals([Signal({'value': read})])
            self.logger.debug('Gage Reading: ' + str(read) + ' mils')
        self._connect_gage()
