import os
import math

# Const
HALFMAX_LOADED_PACKET = 2500
MAX_DATA_SIZE = 32767

# class that have function split data/file,
# checking file checksum, and write data into file
class FileManagerSender:
    def __init__(self, file_path=''):
        self.file_path = file_path
        self.total_chunk = self.calculateTotalChunk()

    def calculateTotalChunk(self):
        cnt = 0
        with open(self.file_path, 'rb') as f:
            chunk = f.read(MAX_DATA_SIZE)
            while chunk:
                cnt += 1
                chunk = f.read(MAX_DATA_SIZE)
        return cnt
    
    def getDataChunk(self, chunk_idx):
        with open(self.file_path, 'rb') as f:
            f.seek(chunk_idx * MAX_DATA_SIZE)
            return f.read(MAX_DATA_SIZE)
        
    
if __name__ == "__main__":
    pass
