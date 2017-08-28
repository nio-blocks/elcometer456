from unittest.mock import patch
from threading import Event

from nio.block.terminals import DEFAULT_TERMINAL
from nio.testing.block_test_case import NIOBlockTestCase
from nio.util.discovery import not_discoverable

from ..elcometer456_block import Elcometer456


@not_discoverable
class ReadEvent(Elcometer456):

    def __init__(self, event):
        super().__init__()
        self._event = event

    def notify_signals(self, signals):
        super().notify_signals(signals)
        self._event.set()


class TestElcometer456(NIOBlockTestCase):

    reading = b'   3.14 mil  N1    \r\n'
    value = 3.14

    def test_default_read(self):
        e = Event()
        blk = ReadEvent(e)
        self.configure_block(blk, {})
        with patch('serial.Serial') as mock_serial:
            mock_serial.return_value.readline.return_value = self.reading
            mock_serial.return_value.isOpen.return_value = True
            self.configure_block(blk, {})
            blk.start()
            # wait for notify_signals
            e.wait(0.1)
        blk.stop()
        if self.value == 3.14:
            # signals are only notified if data value is valid
            self.assertDictEqual(
                self.last_notified[DEFAULT_TERMINAL][0].to_dict(), {
                    'value': self.value
                }
            )
            blk._serial.write.assert_called_with(b"O")
        elif self.value:
            blk._serial.write.assert_called_with(b"O")
        else:
            # write only happens if data has been read
            blk._serial.write.assert_not_called()


class TestElcometer456_BadData(TestElcometer456):

    reading = b'     ---      F1    \r\n'
    value = '---'


class TestElcometer456_ReallyBadData(TestElcometer456):

    reading = b'TestingWeirdStuff\r\n'
    value = 'TestingWeirdStuff'


class TestElcometer456_EmptyData(TestElcometer456):

    reading = b''
    value = ''
