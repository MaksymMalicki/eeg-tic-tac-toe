import serial
from eeg_data_parser.eeg_parser import EegParser

ser = serial.Serial('/dev/tty.BrainLink_Lite', 9600)
parser = EegParser()
while True:
    line = ser.readline()
    parser.parse_eeg_data(line)







