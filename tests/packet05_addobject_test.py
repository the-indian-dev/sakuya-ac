import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.PacketManager.packets.FSNETCMD_ADDOBJECT import FSNETCMD_ADDOBJECT

class TestFSNETCMD_ADDOBJECT(unittest.TestCase):

    def test_decode(self):
        buffer = b'\x05\x00\x00\x00\x01\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x00R\x0c^E\x00\x00\x00\x00H\x85%E\x1d\x96\xcb\xbf\x00\x00\x00\x00\x00\x00\x00\x80HANGER\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\xd7\xa3dB'

        packet = FSNETCMD_ADDOBJECT(buffer)
        self.assertEqual(packet.object_type, 1)
        self.assertEqual(packet.net_type, 1)
        self.assertEqual(packet.object_id, 65538)
        self.assertEqual(packet.iff, 0)
        self.assertEqual(packet.pos, [3552.77001953125, 0.0, 2648.330078125])
        self.assertEqual(packet.atti, [-1.590518593788147, 0.0, -0.0])
        self.assertEqual(packet.identifier, 'HANGER')
        self.assertEqual(packet.substrname, '')
        self.assertEqual(packet.ysfid, 0)
        self.assertEqual(packet.flags, 0)
        self.assertEqual(packet.flags0, 32768)
        self.assertEqual(packet.outsideRadius, 57.15999984741211)

    def test_encode(self):
        buffer = FSNETCMD_ADDOBJECT.encode(
            object_type=1, net_type=1, object_id=65538, iff=0, pos=[3552.77001953125, 0.0, 2648.330078125],
            atti=[-1.590518593788147, 0.0, -0.0], identifier='HANGER', substrname='', ysfid=0,
            flags=0, flags0=32768, outside_radius=57.15999984741211
        )
        expected_buffer = b'\x05\x00\x00\x00\x01\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x00R\x0c^E\x00\x00\x00\x00H\x85%E\x1d\x96\xcb\xbf\x00\x00\x00\x00\x00\x00\x00\x80HANGER\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\xd7\xa3dB'
        self.assertEqual(buffer, expected_buffer)



if __name__ == '__main__':
    unittest.main()