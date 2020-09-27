import os
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

    def addData(self, seqnum, data):
        self.data.append(data)
        self.sequence.append(seqnum)
        self.numpackets += 1

    def orderData(self):
        new_sequence = [x for x in range(self.numpackets)]
        new_data = [b'' for x in range(self.numpackets)]
        for idx, i in enumerate(self.sequence):
            new_data[i] = self.data[idx]
        self.data = new_data
        self.sequence = new_sequence

    def writeFile(self):
        self.orderData()
        self.checksum = self.generateChecksum()
        all_data = b''.join(self.data)
        with open(self.metadata['name'], 'wb') as f:
            f.write(all_data)
        print(f'File <{self.metadata["name"]}> written with checksum: 0x{self.checksum:04x}')

    def addFile(self, file_path):
        self.file_path = file_path
        self.initializeData()
        self.checksum = self.generateChecksum()
    
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

    def generateChecksum(self):
        all_data = b''.join(self.data)
        byte_all_data = self.metadata['size']
        checksum = 0
        for i in range(0, byte_all_data, 2):
            data_bits = int.from_bytes(all_data[i:i+2], byteorder='big')
            checksum ^= data_bits
        return checksum

# testing purposes    
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
    # dump(file_manager)
    file_manager.metadata['name'] = 'spesifikasi2.pdf'
    shuffleOrder(file_manager)
    file_manager.writeFile()
