from eeg_parser import EegParser

parser = EegParser()
test_packet = b'\xaa\xaa\x08\x02\x20\x01\x7e\x04\x12\x05\x60\xe3'
parser.parse_eeg_data(test_packet)

