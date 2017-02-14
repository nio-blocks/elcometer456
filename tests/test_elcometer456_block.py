from unittest.mock import patch
from collections import defaultdict
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..elcometer456_block import Elcometer456


class TestElcometer456(NIOBlockTestCase):

    def test_default_read(self):
        blk = Elcometer456()
        with patch('serial.Serial') as mock_serial:
            mock_serial.return_value.readline.return_value = b'   3.14 mil  N1    \r\n'
            mock_serial.return_value.isOpen.return_value = True
            self.configure_block(blk, {})
        blk.start()
        from time import sleep
        sleep(1)
        blk.stop()
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(), {
            "value": 3.14
        })
        blk._serial.write.assert_called_with(b"O")

    def test_bad_reading(self):
        blk = Elcometer456()
        with patch('serial.Serial') as mock_serial:
            mock_serial.return_value.readline.return_value = b'     ---      F1    \r\n'
            mock_serial.return_value.isOpen.return_value = True
            self.configure_block(blk, {})
        blk.start()
        from time import sleep
        sleep(1)
        blk.stop()
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(), {
            "value": b''
        })
        blk._serial.write.assert_called_with(b"O")
