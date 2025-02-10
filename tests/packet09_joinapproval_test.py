import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.PacketManager.packets.FSNETCMD_JOINAPPROVAL import FSNETCMD_JOINAPPROVAL

class TestFSNETCMD_JOINAPPROVAL(unittest.TestCase):

    def test_decode(self):
        buffer = b'\t\x00\x00\x00'
        packet = FSNETCMD_JOINAPPROVAL(buffer)
        self.assertEqual(packet.buffer, buffer)

    def test_encode(self):
        buffer = FSNETCMD_JOINAPPROVAL.encode()
        expected_buffer = b'\t\x00\x00\x00'
        self.assertEqual(buffer, expected_buffer)

    def test_encode_with_size(self):
        buffer = FSNETCMD_JOINAPPROVAL.encode(with_size=True)
        expected_buffer = b'\x04\x00\x00\x00\t\x00\x00\x00'
        self.assertEqual(buffer, expected_buffer)

if __name__ == '__main__':
    unittest.main()