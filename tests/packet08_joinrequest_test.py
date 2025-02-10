import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.PacketManager.packets.FSNETCMD_JOINREQUEST import FSNETCMD_JOINREQUEST

class TestFSNETCMD_JOINREQUEST(unittest.TestCase):

    def test_decode(self):
        buffer = b'\x08\x00\x00\x00\x02\x00\x00\x00EUROFIGHTER_TYPHOON\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00RW36_01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00K\x00\x00\x00'
        packet = FSNETCMD_JOINREQUEST(buffer)
        self.assertEqual(packet.iff,2)
        self.assertEqual(packet.aircraft, 'EUROFIGHTER_TYPHOON')
        self.assertEqual(packet.start_pos, 'RW36_01')
        self.assertEqual(packet.fuel, 75)
        self.assertEqual(packet.smoke,0)

    def test_encode(self):
        iff = 2
        aircraft = 'EUROFIGHTER_TYPHOON'
        start_pos = 'NORTH10000_01'
        fuel = 75
        smoke = 0
        buffer = FSNETCMD_JOINREQUEST.encode(iff, aircraft, start_pos, fuel, smoke)
        expected_buffer = b'\x08\x00\x00\x00\x02\x00\x00\x00EUROFIGHTER_TYPHOON\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00NORTH10000_01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00K\x00\x00\x00'
        self.assertEqual(buffer, expected_buffer)


if __name__ == '__main__':
    unittest.main()