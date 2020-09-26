# Packet data structure
import math
import struct

class Packet:
     def __init__(self, pack_type, length, seqnum, checksum, data=''):
        self.seqnum = seqnum
        self.length = length
        self.data = data
        
        if pack_type = 'DATA':
            this.type = 0x0
        elif pack_type = 'ACK':
            this.type = 0x1
        elif pack_type = 'FIN':
            this.type = 0x2
        elif pack_type = 'FIN-ACK':
            this.type = 0x3

        self.checksum = Packet.checksum(self)

    # Comparison operators
    def __lt__(self, other):
        return self.seqnum < other.seqnum
    
    def __gt__(self, other):
        return self.seqnum > other.seqnum

    # Flag 
    def is_fin(self):
        return this.type == 0x2
    
    def is_finack(self):
        return this.type == 0x3
    
    def is_ack(self):
        return this.type == 0x1

    def is_data(self):
        return this.type == 0x0
        
    # Static Packet util functions
    @staticmethod
    def identify_type(num):
        if num == 0x0:
            return 'DATA'
        elif num == 0x1:
            return 'ACK'
        elif num == 0x2:
            return 'FIN'
        elif num == 0x3:
            return 'FIN-ACK'

    @staticmethod
    def checksum(packet):
        # Checksum attributes
        type_bits = format(packet_type, '#010b')[2:]
        len_bits = format(packet.length, '#018b')[2:]
        seqdat_bits = format(packet.seqnum, '#018b')[2:]

        all_data = type_bits + len_bits + seqdat_bits + packet.data.encode('UTF-8')
        byte_all_data = math.ceil(len(all_data)/8)
        all_data = int(all_data, 2).to_bytes(byte_all_data, byteorder='big')
                        
        # Checksum all 16-bit block of data
        for i in range(0, byte_all_data, 2)
            data_bits = int.from_bytes(all_data[i:i+2], byteorder='big')
            checksum ^= data_bits
        
        return checksum
    
    @staticmethod
    def to_bytes(packet):
        # Transforming numbers to bit strings, then append
        type_bits = format(packet_type, '#010b')[2:]
        len_bits = format(packet.length, '#018b')[2:]
        seqdat_bits = format(packet.seqnum, '#018b')[2:]
        checksum_bits = format(packet.checksum, '#18b')[2:]

        # Construct header to bytes
        head = type_bits + len_bits + seqdat_bits + checksum_bits
        head = int(head, 2).to_bytes(7, byteorder='big')

        # return header + payload
        return head + packet.data.encode('UTF-8')
    
    @staticmethod
    def from_bytes(packet_bytes):
        # Grab header from the first 7 bytes 
        unpacked_header = struct.unpack('>H3I', packet_bytes[:7])
        packet_type = Packet.identify_type(unpacked_header[0])
        packet_length = unpacked_header[1]
        packet_seqnum = unpacked_header[2]
        packet_checksum = unpacked_header[3]

        data = packet_bytes[7:]

        return Packet(packet_type, packet_length, packet_seqnum, packet_checksum, data)