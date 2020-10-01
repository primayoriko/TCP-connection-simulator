import os
import math

# Const
MAX_LOADED_PACKET_HEAD = 500
MAX_LOADED_PACKET_TAIL = 3500
MAX_DATA_SIZE = 32767

# class that have function split data/file,
# checking file checksum, and write data into file
class FileManager:
    def __init__(self, file_path='', caching=True, mode='sending'):
        self.metadata = {'name': 'downloaded', 'size': 0}
        if mode == 'sending':
            self.caching = caching
            self.changeFile(file_path)
        elif mode == 'receiving':
            self.firstWrite = True
            self.size_downloaded = 0
            self.total_chunk = 0
    
    def useCaching(self, caching):
        self.caching = caching
        if self.caching:
            self.loadPacket(MAX_LOADED_PACKET_HEAD)

    def changeFile(self, file_path):
        self.file_path = file_path
        self.metadata['name'] = os.path.basename(self.file_path)
        self.metadata['size'] = os.path.getsize(self.file_path)
        self.total_chunk = math.ceil(self.metadata['size'] / 32767)
        if self.caching:
            self.loadPacket(MAX_LOADED_PACKET_HEAD)

    def isLoaded(self, index):
        if self.caching:
            return index >= self.lower_bound and index <= self.upper_bound
        else:
            return False

    def loadPacket(self, mid):
        if not self.caching:
            return

        self.data = []
        self.lower_bound = max(0, mid - MAX_LOADED_PACKET_HEAD)
        self.upper_bound = min(mid + MAX_LOADED_PACKET_TAIL, self.total_chunk)

        with open(self.file_path, 'rb') as f:
            f.seek(self.lower_bound * MAX_DATA_SIZE)
            seg_num = self.lower_bound
            while (seg_num <= self.upper_bound):
                data_chunk = f.read(MAX_DATA_SIZE)
                if(not data_chunk):
                    break
                
                self.data.append(data_chunk)
                seg_num += 1

            # self.upper_bound = min(self.upper_bound, seg_num)
            print(
                    "Load chunk(s) from indexes {0} until {1} success!"
                        .format(self.lower_bound, self.upper_bound)
                )
    
    def getChunk(self, index):
        if not self.caching:
            with open(self.file_path, 'rb') as f:
                if(index > 0):
                    index -= 1
                    f.seek(index * MAX_DATA_SIZE)

                return f.read(MAX_DATA_SIZE)
                
        if(not self.isLoaded(index)):
            self.loadPacket(index)

        return self.data[index - self.lower_bound]

    # Add Metadata Information
    def addMetadata(self, name, size):
        self.metadata['name'] = name
        self.metadata['size'] = size
        self.total_chunk = math.ceil(self.metadata['size'] / 32767)
    
    # RECEIVER: Write data per packet received
    def writePacket(self, seqnum, data):
        self.size_downloaded += len(data)
        if self.metadata['name'] == 'downloaded':
            self.metadata['size'] += len(data)
            self.total_chunk += 1
            print(f'Total file data written: {self.size_downloaded} | total numpackets received: {self.total_chunk}')    
        else:
            print(f'File data written: {self.size_downloaded/self.metadata["size"]*100:3.0f}% {self.size_downloaded}/{self.metadata["size"]}')
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

if __name__ == "__main__":
    pass
