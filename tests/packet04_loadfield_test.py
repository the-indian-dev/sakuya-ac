import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.PacketManager.packets.FSNETCMD_LOADFIELD import FSNETCMD_LOADFIELD
from struct import pack

class TestFSNETCMD_LOADFIELD(unittest.TestCase):

    def test_decode(self):
        buffer = b'\x04\x00\x00\x00ISLAND_GOURD\x00\xc39\x00\xe0\x1ff\x00\r\x00\x00\x00\r\x00\x00\x00\x10\xc49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        packet = FSNETCMD_LOADFIELD(buffer)
        self.assertEqual(packet.fieldShortName, 'ISLAND_GOURD')
        self.assertEqual(packet.flags, 0)
        self.assertEqual(packet.pos, [0, 0, 0])
        self.assertEqual(packet.atti, [0, 0,0])

    def test_encode(self):
        field = b'ISLAND_GOURD\x00\xc39\x00\xe0\x1ff\x00\r\x00\x00\x00\r\x00\x00\x00\x10\xc49\x00'
        flags = 0
        pos = [0, 0, 0]
        atti = [0, 0, 0]
        buffer = FSNETCMD_LOADFIELD.encode(field, flags, pos, atti)
        expected_buffer = b'\x04\x00\x00\x00ISLAND_GOURD\x00\xc39\x00\xe0\x1ff\x00\r\x00\x00\x00\r\x00\x00\x00\x10\xc49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.assertEqual(buffer, expected_buffer)

    def test_encode_with_size(self):
        field = b'ISLAND_GOURD\x00\xc39\x00\xe0\x1ff\x00\r\x00\x00\x00\r\x00\x00\x00\x10\xc49\x00'
        flags = 0
        pos = [0, 0, 0]
        atti = [0, 0, 0]
        buffer = FSNETCMD_LOADFIELD.encode(field, flags, pos, atti, with_size=True)
        expected_buffer = b'@\x00\x00\x00\x04\x00\x00\x00ISLAND_GOURD\x00\xc39\x00\xe0\x1ff\x00\r\x00\x00\x00\r\x00\x00\x00\x10\xc49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.assertEqual(buffer, expected_buffer)

if __name__ == '__main__':
    unittest.main()