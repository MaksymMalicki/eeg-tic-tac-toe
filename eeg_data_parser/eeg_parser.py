class EegParser:
    def __init__(self):
        ## helper states
        self.SYNC_STATE = 1
        self.P_LENGTH_STATE = 2
        self.PAYLOAD_STATE = 3
        self.CHECKSUM_STATE = 4
        self.V_LENGTH_STATE = 5

        ## helper attributes
        self.current_state = self.SYNC_STATE
        self.v_length = 1
        self.v_length_counter = 0
        self.payload_length_counter = 0
        self.is_code = True
        self.current_data = []

        # data bytes
        self.sync_byte = 170  # 0xAA
        self.sync_bytes_count = 0
        self.payload_length = None
        self.payload_data_counter = 0
        self.payload_data = []
        self.payload_codes = []
        self.checksum = None
        self.calculated_checksum = 0

    def parse_eeg_data(self, packet):
        parsed_packet = [byte for byte in packet]
        print(parsed_packet)
        for byte in parsed_packet:
            if self.current_state == self.SYNC_STATE:
                if byte == self.sync_byte:
                    self.sync_bytes_count += 1
                    if self.sync_bytes_count == 2:
                        self.current_state = self.P_LENGTH_STATE
                        print("1.SYNCED")
                else:
                    self.sync_bytes_count = 0
                    print("1.NOT SYNCED")

            elif self.current_state == self.P_LENGTH_STATE:
                self.payload_length = byte
                if self.payload_length > 170:       # DOCS "Step by step guide to parsing a packet"
                    self.current_state = self.SYNC_STATE
                    print("2.PAYLOAD TOO LARGE (PLENGTH>170)")
                self.current_state = self.PAYLOAD_STATE
                print(f"2.PAYLOAD LENGTH: {self.payload_length}")

            elif self.current_state == self.PAYLOAD_STATE:
                # The code is always sent first, that's why is_code is True by default
                # If the code was sent, whe check if it's greater than 0x7F
                # If yes, then we have extended code, and we assign the custom v_length in the V_LENGTH_STATE
                # If not, then the next byte will be data byte, that's why v_length == 1
                if self.is_code:
                    if byte > 127:
                        self.current_state = self.V_LENGTH_STATE
                        print("3.EXTENDED CODE")
                    else:
                        self.v_length = 1
                    self.is_code = not self.is_code
                    self.payload_codes.append(byte)
                    print(f"PAYLOAD CODES: {self.payload_codes}")
                else:
                    self.current_data.append(byte)
                    self.v_length_counter += 1
                    if self.v_length_counter == self.v_length:
                        # setting
                        self.is_code = not self.is_code
                        self.payload_data.append(self.current_data)
                        print(f"PAYLOAD VALUE: {self.payload_data}")
                        # resetting
                        self.v_length_counter = 0
                        self.current_data = []
                self.payload_length_counter += 1
                if self.payload_length_counter == self.payload_length:
                    self.current_state = self.CHECKSUM_STATE
                    self.v_length = 1
                    self.v_length_counter = 0
                    self.is_code = True

            elif self.current_state == self.V_LENGTH_STATE:
                self.v_length = byte
                self.current_state = self.PAYLOAD_STATE
                print(f"VLENGTH: {self.v_length}")

            elif self.current_state == self.CHECKSUM_STATE:
                self.checksum = byte
                print(self.payload_data, self.payload_codes)
                for data_row in self.payload_data:
                    for value in data_row:
                        self.calculated_checksum += value
                self.calculated_checksum += sum(code for code in self.payload_codes)
                self.calculated_checksum = (255 - self.calculated_checksum) & 0xFF
                print(self.calculated_checksum)
                if self.checksum == self.calculated_checksum:
                    print(self.checksum, self.payload_length, self.payload_data)
                self.sync_bytes_count = 0
                self.payload_length = None
                self.payload_data = []
                self.checksum = None
                self.current_state = self.SYNC_STATE

    def decode_eeg_code(self, code):
        # single byte codes
        if code == bytes(0x02):
            print('POOR SIGNAL QUALITY: ')
        elif code == bytes(0x03):
            print('HEART_RATE (0-255)')
        elif code == bytes(0x04):
            print("ATTENTION eSense (0 to 100)")
        elif code == bytes(0x05):
            print("MEDITATION eSense (0 to 100)")
        elif code == bytes(0x06):
            print("8BIT_RAW Wave Value (0-255)")
        elif code == bytes(0x07):
            print("RAW_MARKER Section Start (0)")

        # multi byte codes
        elif code == bytes(0x80):
            print("RAW Wave Value: a single big-endian 16-bit two's-compliment signed")
        elif code == bytes(0x81):
            pass
        elif code == bytes(0x83):
            pass
        elif code == bytes(0x86):
            pass
