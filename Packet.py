# Packet data structure

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
        checksum = 0

        # Checksum attributes
        checksum = checksum ^ packet.type ^ packet.length ^ packet.seqnum
        
        # Checksum all 16-bit block of data
        data_bits = int.from_bytes(packet.data, byteorder='big')

        while data_bits:
            checksum ^= data_bits & 0xFFFF
            data_bits = data_bits >> 16
        
        return checksum