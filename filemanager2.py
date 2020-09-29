import os
import math

# Const
HALFMAX_LOADED_PACKET = 2500
MAX_DATA_SIZE = 32774

# class that have function split data/file,
# checking file checksum, and write data into file
class FileManager:
    def __init__(self, file_path=''):
        self.changeFile(file_path)

    def changeFile(self, file_path)
        self.file_path = file_path
        self.lower_bound = 0
        self.upper_bound = 2 * HALFMAX_LOADED_PACKET
        self.loadPacket(HALFMAX_LOADED_PACKET)

    def isLoaded(self, index):
        return index >= self.lower_bound 
            and index <= self.upper_bound

    def loadPacket(self, mid):
        self.data = []
        self.lower_bound = max(0, mid - HALFMAX_LOADED_PACKET)
        self.upper_bound = mid + HALFMAX_LOADED_PACKET
        self.metadata['name'] = os.path.basename(self.file_path)
        self.metadata['size'] = os.path.getsize(self.file_path)
        # size_chunked = 0

        with open(self.file_path, 'rb') as f:
            for i in range(self.lower_bound):
                data_chunk = f.read(MAX_DATA_SIZE)

            seg_num = self.lower_bound
            while (seg_num <= self.upper_bound):
                data_chunk = f.read(MAX_DATA_SIZE)
                if(not data_chunk):
                    break
                
                self.data.append(data_chunk)
                seg_num += 1
                # size_chunked += len(data_chunk)
                # if self.numpackets % 10 == 0:
                #     print(f'Processing file: {size_chunked/self.metadata["size"]*100:3.0f}% [{size_chunked} readed out of {self.metadata["size"]}]')

            self.upper_bound = min(self.upper_bound, seg_num)
            print(
                    "Load chunk(s) from indexes {0} until {1} success!"
                        .format(self.lower_bound, self.upper_bound)
                )
    
    def getChunk(self, index):
        if(not self.isLoaded(index)):
            self.loadPacket(index)

        return self.data[index - self.lower_bound]

    @staticmethod
    def isMaxLoaded(packets):
        return len(packets) >= 2 * HALFMAX_LOADED_PACKET

    def writeFile(self):
        pass

if __name__ == "__main__":
    pass
