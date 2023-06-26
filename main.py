import serial
import sys
from eeg_data_parser.eeg_parser import EegParser

parser = EegParser()

if sys.platform.startswith('win'):
    ser = serial.Serial(port='COM6')

elif sys.platform.startswith('darwin'):
    ser = serial.Serial('/dev/tty.BrainLink_Lite', 9600)

while True:
    line = ser.readline()
    parser.parse_eeg_data(line)






