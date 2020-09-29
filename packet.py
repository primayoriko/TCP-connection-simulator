# Packet data structure
import math
import struct

class Packet:
    def __init__(self, pack_type, length=0, seqnum=-1, checksum=-1, data=''):
        self.seqnum = seqnum
        self.length = length
        self.data = data

        if pack_type == 'DATA':
            self.type = 0x0
        elif pack_type == 'ACK':
            self.type = 0x1
        elif pack_type == 'FIN':
            self.type = 0x2
        elif pack_type == 'FIN-ACK':
            self.type = 0x3

        self.checksum = checksum

    # Comparison operators
    def __lt__(self, other):
        return self.seqnum < other.seqnum

    def __gt__(self, other):
        return self.seqnum > other.seqnum

    # Flag
    def is_fin(self):
        return self.type == 0x2

    def is_finack(self):
        return self.type == 0x3

    def is_ack(self):
        return self.type == 0x1

    def is_data(self):
        return self.type == 0x0

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
        all_data = struct.pack('>b2H', packet.type, packet.length, packet.seqnum)

        if isinstance(packet.data, str):
            all_data += packet.data.encode('UTF-8')
        else:
            all_data += packet.data


        # Checksum all 16-bit block of data
        checksum = 0
        for i in range(0, len(all_data), 2):
            data_bits = int.from_bytes(all_data[i:i+2], byteorder='big')
            checksum ^= data_bits

        return checksum

    @staticmethod
    def to_bytes(packet):
        # Transforming numbers to bit strings, then append
        head = struct.pack('>b3H', packet.type, packet.length, packet.seqnum, Packet.checksum(packet))

        # return header + payload
        if isinstance(packet.data, str):
            return head + packet.data.encode('UTF-8')
        else:
            return head + packet.data

    @staticmethod
    def from_bytes(packet_bytes):
        # Grab header from the first 7 bytes
        unpacked_header = struct.unpack('>b3H', packet_bytes[:7])
        packet_type = Packet.identify_type(unpacked_header[0])
        packet_length = unpacked_header[1]
        packet_seqnum = unpacked_header[2]
        packet_checksum = unpacked_header[3]

        data = packet_bytes[7:]

        return Packet(packet_type, packet_length, packet_seqnum, packet_checksum, data)

class Metadata:
    """
    8 bits type
    8 bits length
    32 bits file_size
    16 bits checksum
    x bits file_name
    """
    def __init__(self, file_name, file_size, checksum=-1):
        self.type = 0x4
        self.length = len(file_name)
        self.file_size = file_size
        self.checksum = checksum
        self.file_name = file_name
    
    @staticmethod
    def checksum(packet):
        # Checksum attributes
        all_data = struct.pack('>2bI', packet.type, packet.length, packet.file_size)

        if isinstance(packet.file_name, str):
            all_data += packet.file_name.encode('UTF-8')
        else:
            all_data += packet.file_name

        # Checksum all 16-bit block of data
        checksum = 0
        for i in range(0, len(all_data), 2):
            data_bits = int.from_bytes(all_data[i:i+2], byteorder='big')
            checksum ^= data_bits

        return checksum

    @staticmethod
    def to_bytes(packet):
        # Transforming numbers to bit strings, then append
        head = struct.pack('>2bIH', packet.type, packet.length, packet.file_size, Metadata.checksum(packet))

        # return header + payload
        if isinstance(packet.file_name, str):
            return head + packet.file_name.encode('UTF-8')
        else:
            return head + packet.file_name

    @staticmethod
    def from_bytes(packet_bytes):
        # Grab header from the first 8 bytes
        unpacked_header = struct.unpack('>2bIH', packet_bytes[:8])
        packet_type = 0x4
        packet_length = unpacked_header[1]
        packet_file_size = unpacked_header[2]
        packet_checksum = unpacked_header[3]

        packet_file_name = packet_bytes[8:].decode('UTF-8')

        return Metadata(packet_file_name, packet_file_size, packet_checksum)

def unpackPacket(packet_bytes):
    if packet_bytes[0] == 4:
        packet = Metadata.from_bytes(packet_bytes)
    else:
        packet = Packet.from_bytes(packet_bytes)

    return packet