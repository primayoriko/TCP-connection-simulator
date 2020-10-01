import os
import math

# class that have function split data/file,
# checking file checksum, and write data into file
class FileManager:
    def __init__(self):
        self.data = []
        self.sequence = []
        self.metadata = {'name': 'downloaded', 'size': 0}
        self.size_downloaded = 0
        self.numpackets = 0
        self.firstWrite = True

    # Adding data
    def addData(self, seqnum, data):
        self.writePacket(seqnum, data)
        self.size_downloaded += len(data)
        if self.metadata['name'] == 'downloaded':
            self.metadata['size'] += len(data)
            self.numpackets += 1
            print(f'Total file data written: {self.size_downloaded} | total numpackets received: {self.numpackets}')    
        else:
            print(f'File data written: {self.size_downloaded/self.metadata["size"]*100:3.0f}% {self.size_downloaded}/{self.metadata["size"]}')

    # Optimization to write file per packet if packet size is known beforehand
    def addMetadata(self, name, size):
        self.metadata['name'] = name
        self.metadata['size'] = size
        self.numpackets = self.totalPacketNeeded()

    # Get total packet needed if size is known
    def totalPacketNeeded(self):
        return math.ceil(self.metadata['size'] / 32767)

    # Write data per packet received
    def writePacket(self, seqnum, data):
        file_offset = seqnum * 32767
        output_file = os.path.join('.', 'out', self.metadata['name'])
        if self.firstWrite:
            self.firstWrite = False
            with open(output_file, 'wb') as f:
                f.seek(file_offset)
                f.write(data)
        else:
            with open(output_file, 'r+b') as f:
                f.seek(file_offset)
                f.write(data)

    # Check if File Manager has all the data if the size is known
    def isComplete(self):
        return self.metadata['size'] == self.size_downloaded

    # Adding file for sender
    def addFile(self, file_path):
        self.file_path = file_path
        self.initializeData()

    # Splitting file and get basic metadata info
    def initializeData(self):
        self.metadata['name'] = os.path.basename(self.file_path)
        self.metadata['size'] = os.path.getsize(self.file_path)
        size_chunked = 0
        with open(self.file_path, 'rb') as f:
            data_chunk = f.read(32767)
            while data_chunk:
                self.data.append(data_chunk)
                self.numpackets += 1
                size_chunked += len(data_chunk)
                if self.numpackets % 10 == 0:
                    print(f'Processing file: {size_chunked/self.metadata["size"]*100:3.0f}% [{size_chunked} readed out of {self.metadata["size"]}]')
                data_chunk = f.read(32767)
        print('Processing file done!')
        self.sequence = [x for x in range(self.numpackets)]

if __name__ == "__main__":
    # from dumper import dump
    import random
    file_path = 'Adobe.Photoshop.Lightroom.Classic.v8.4.1.10.Full.Version.7z'
    file_manager = FileManager()
    file_manager.addFile(file_path)
    # dump(file_manager)
    # shuffleOrder(file_manager)
    file_manager.writeFile()
