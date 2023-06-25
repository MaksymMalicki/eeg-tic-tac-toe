import serial
from eeg_data_parser.eeg_data_parser import EegDataParser
ser = serial.Serial('/dev/tty.BrainLink_Lite', 9600)
parser = EegDataParser()
while True:
    line = ser.readline()
    parser.parse_eeg_data(line)







