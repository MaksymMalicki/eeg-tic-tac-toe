import unittest
from eeg_parser import EegParser


class TestEegDataParser(unittest.TestCase):

    def test_parse_eeg_data_single_packet(self):
        parser = EegParser()
        test_packet = b'\xaa\xaa\x04\x01\x02\x03\x04'
        parser.parse_eeg_data(test_packet)
        self.assertEqual(parser.current_state, parser.CHECKSUM_STATE)
        self.assertEqual(parser.payload_length, 4)
        self.assertEqual(parser.payload_codes, [1, 3])
        self.assertEqual(parser.payload_data, [[2], [4], ])

    def test_parse_eeg_data_multiple_packets(self):
        parser = EegParser()
        test_packet1 = b'\xaa\xaa\x04'
        test_packet2 = b'\x01\x02\x03\x04'
        test_packet3 = b'\xf5'
        parser.parse_eeg_data(test_packet1)
        parser.parse_eeg_data(test_packet2)
        self.assertEqual(parser.payload_codes, [1, 3])
        self.assertEqual(parser.payload_data, [[2], [4]])
        self.assertEqual(parser.payload_length, 4)
        parser.parse_eeg_data(test_packet3)
        self.assertEqual(parser.current_state, parser.SYNC_STATE)

    def test_parse_eeg_data_invalid_packets(self):
        pass

    def test_parse_eeg_data_incomplete_packets(self):
        pass


if __name__ == '__main__':
    unittest.main()
