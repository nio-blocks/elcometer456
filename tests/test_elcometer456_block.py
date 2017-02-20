from unittest.mock import patch
from collections import defaultdict
from threading import Event
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..elcometer456_block import Elcometer456


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
            e.wait(1.5)
        blk.stop()
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(), {
                'value': self.value
            }
        )
        blk._serial.write.assert_called_with(b"O")

class TestElcometer456_BadData(TestElcometer456):

    reading = b'     ---      F1    \r\n'
    value = 0
