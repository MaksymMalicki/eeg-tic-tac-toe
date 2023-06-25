class EegDataParser:
    def __init__(self):
        self.SYNC_STATE = 1
        self.P_LENGTH_STATE = 2
        self.PAYLOAD_STATE = 3
        self.CHECKSUM_STATE = 4

        self.current_state = self.SYNC_STATE

        self.sync_byte = 170 #0xAA
        self.sync_bytes_count = 0
        self.payload_length = None
        self.payload_data = []
        self.checksum = None

    def parse_eeg_data(self, packet):
        parsed_packet = [byte for byte in packet]
        for byte in parsed_packet:
            if self.current_state == self.SYNC_STATE:
                if byte == self.sync_byte:
                    self.sync_bytes_count += 1
                    if self.sync_bytes_count == 2:
                        self.current_state = self.P_LENGTH_STATE
                else:
                    self.sync_bytes_count = 0

            elif self.current_state == self.P_LENGTH_STATE:
                self.payload_length = byte
                self.current_state = self.PAYLOAD_STATE

            elif self.current_state == self.PAYLOAD_STATE:
                self.payload_data.append(byte)
                if len(self.payload_data) == self.payload_length:
                    self.current_state = self.CHECKSUM_STATE

            elif self.current_state == self.CHECKSUM_STATE:
                self.checksum = byte
                calculated_checksum = sum(self.payload_data) ^ 0xFF
                if self.checksum == calculated_checksum:
                    print(self.checksum, self.payload_length, self.payload_data)
                self.sync_bytes_count = 0
                self.payload_length = None
                self.payload_data = []
                self.checksum = None
                self.current_state = self.SYNC_STATE

    def decode_eeg_code(self, code):
        # single byte codes
        if code == bytes(0x02):
            print('POOR SIGNAL QUALITY 0-255')
        elif code == bytes(0x03):
            pass
        elif code == bytes(0x04):
            pass
        elif code == bytes(0x05):
            pass
        elif code == bytes(0x06):
            pass
        elif code == bytes(0x07):
            pass

        # multi byte codes
        elif code == bytes(0x80):
            pass
        elif code == bytes(0x81):
            pass
        elif code == bytes(0x83):
            pass
        elif code == bytes(0x86):
            pass
