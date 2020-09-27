import os
import math
from packet import Packet

# class that have function split data/file into packet(s),
# checking packet, and arrange packet(s) into file
class FileManager:
    def __init__(self):
        self.data = []
        self.sequence = []
        self.metadata = {'name': 'downloaded', 'size': 0}
        self.numpackets = 0
        self.checksum = 0
        self.writePerPacket = False

    # Adding data, unordered
    def addData(self, seqnum, data):
        if self.writePerPacket:
            self.writePerPacket(seqnum, data)
            self.size_downloaded += len(data)
        else:
            self.data.append(data)
            self.sequence.append(seqnum)
            self.numpackets += 1
            self.metadata['size'] += len(data)

    # Ordering data before writing to a file
    def orderData(self):
        new_sequence = [x for x in range(self.numpackets)]
        new_data = [b'' for x in range(self.numpackets)]
        for idx, i in enumerate(self.sequence):
            new_data[i] = self.data[idx]
        self.data = new_data
        self.sequence = new_sequence

    # Optimization to write file per packet if packet size is known beforehand    
    def addMetadata(self, name, size):
        self.metadata['name'] = name
        self.metadata['size'] = size
        self.numpackets = self.totalPacketNeeded()
        self.writePerPacket = True
        self.size_downloaded = 0

    # Get total packet needed if size is known
    def totalPacketNeeded(self):
        return math.ceil(self.metadata['size'] / 32767)

    # Write data per packet received
    def writePacket(self, seqnum, data):
        file_offset = seqnum * 32767
        output_file = os.path.join('.', 'out', self.metadata['name'])
        with open(output_file, 'wb') as f:
            f.seek(file_offset)
            f.write(data)

    # Check if File Manager has all the data if the size is known
    def isComplete(self):
        return self.metadata['size'] == self.size_downloaded

    # Writing all data to ./out/downloaded and print the checksum in 4 digit hex
    def writeFile(self):
        self.orderData()
        self.checksum = self.generateChecksum()
        all_data = b''.join(self.data)
        output_file = os.path.join('.', 'out', self.metadata['name'])
        with open(output_file, 'wb') as f:
            f.write(all_data)
        print(f'File <{self.metadata["name"]}> written with checksum: 0x{self.checksum:04x}')

    # Adding file for sender
    def addFile(self, file_path):
        self.file_path = file_path
        self.initializeData()
        self.checksum = self.generateChecksum()
    
    # Splitting file and get basic metadata info
    def initializeData(self):
        self.metadata['name'] = os.path.basename(self.file_path)
        self.metadata['size'] = os.path.getsize(self.file_path)
        with open(self.file_path, 'rb') as f:
            data_chunk = f.read(32767)
            while data_chunk:
                self.data.append(data_chunk)
                self.numpackets += 1
                data_chunk = f.read(32767)
        self.sequence = [x for x in range(self.numpackets)]

    # Generate 16 bit xor checksum for all data
    def generateChecksum(self):
        all_data = b''.join(self.data)
        byte_all_data = self.metadata['size']
        checksum = 0
        for i in range(0, byte_all_data, 2):
            data_bits = int.from_bytes(all_data[i:i+2], byteorder='big')
            checksum ^= data_bits
        return checksum

# TESTING PURPOSES: shuffle data to simulate unordered sequence received
def shuffleOrder(file_manager: FileManager):
    random.shuffle(file_manager.sequence)
    shuffled_data = []
    for i in file_manager.sequence:
        shuffled_data.append(file_manager.data[i])
    file_manager.data = shuffled_data

if __name__ == "__main__":
    # from dumper import dump
    import random
    file_path = 'spesifikasi.pdf'
    file_manager = FileManager()
    file_manager.addFile(file_path)
    print(f'File input checksum: 0x{file_manager.checksum:04x}')
    # dump(file_manager)
    file_manager.metadata['name'] = 'spesifikasi2.pdf'
    shuffleOrder(file_manager)
    file_manager.writeFile()
