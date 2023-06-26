import unittest
from eeg_parser import EegParser


class TestEegDataParser(unittest.TestCase):

    def test_parse_eeg_data_single_packet(self):
        parser = EegParser()
        test_packet = b'\0xaa\0xaa'
        parser.parse_eeg_data(test_packet)
        self.assertEqual(parser.current_state, parser.P_LENGTH_STATE)

    def test_parse_eeg_data_multiple_packets(self):
        parser = EegParser()
        test_packet1 = b'\0xaa\0xaa\0x04'
        test_packet2 = b'\0x01\0x02\0x03\0x04'
        test_packet3 = b'\0x15'
        parser.parse_eeg_data(test_packet1)
        parser.parse_eeg_data(test_packet2)
        parser.parse_eeg_data(test_packet3)
        self.assertEqual(parser.payload_data, [1, 2, 3, 4])
        self.assertEqual(parser.payload_length, 4)
        self.assertEqual(parser.current_state, parser.SYNC_STATE)

    def test_parse_eeg_data_invalid_packets(self):
        pass

    def test_parse_eeg_data_incomplete_packets(self):
        pass


if __name__ == '__main__':
    unittest.main()
