## Parser
### EEG PACKET
[SYNC] [SYNC] [PLENGTH]    [PAYLOAD...]     [CHKSUM]  
_______________________    _____________    ____________  
^^^^^^^^(HEADER)^^^^^^^    ^^(PAYLOAD)^^    ^(CHECKSUM)^  

### HEADER
1. First there are two sync bytes, each with the value of 0xAA
2. Then, there is a PLENGTH (length of the PAYLOAD), which is max 169 (if more - PLENGTH TOO LARGE)
3. The PACKET's max length is 173 (2xSYNC + 1xPLENGTH + 169 + 1xCHECKSUM)
4. There might appear two 0xAA bits in the middle of the packet, but PLENGTH and CHECKSUM combined provide a validation system
### PAYLOAD
1. PAYLOAD parsing should be done after checking the PLENGTH and CHECKSUM
2. PAYLOAD consists of DataRows, each look like this:  
([EXCODE]...) [CODE]  ([VLENGTH])  [VALUE...]  
____________________ ____________ ___________  
^^^^(Value Type)^^^^ ^^(length)^^ ^^(value)^^  
1. The one in parenthesis appear only when the EXCODE (0x55) is provided
2. If CODE<=0x7F, then VALUE is of length 1 byte.
3. If CODE>0x7F, then VLENGTH must be provided, as the VALUE length might be greater than 1 byte.
### CHECKSUM
1. Checksum is calculated as following:
   1. summing all the bytes of the Packet's Data Payload
   2. taking the lowest 8 bits of the sum
   3. performing the bit inverse (one's compliment inverse) on those lowest 8 bits
2. In the end, the calculated check sum must be compared with the provided checksum. If they are different, then the entire packet is invalid.