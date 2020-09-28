# from Packet import Packet
import socket
import sys
from packet import Packet
from filemanager import FileManager

HOST = '127.0.0.1'
PORT = 1338
MAX_SEG_SIZE = 32774
TIMEOUT = 1000

if __name__ == '__main__':
    file_path = sys.argv[1]
    targets = sys.argv[2:]

    file_manager = FileManager()
    file_manager.addFile(file_path)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    sock.listen()
    
    print(file_path)
    print(targets)
    print(f'File input checksum: 0x{file_manager.checksum:04x}')
    print(file_manager.numpackets)

    # Sent packets one by one per target 
    for target in targets:
        success = 0
        arr_succeed = [False for i in range(file_manager.numpackets)]

        # Loop until all data sent
        while(not all(arr_succeed)):
            for i in range(file_manager.numpackets):
                if(not arr_succeed[i]):
                    s.connect((HOST, PORT))
                    sent = False
                    while(not sent):
                        s.sendall(target)
                    arr_succeed[i] = sent
                    success += 1 
            print("Status : " + str(success) + "/" + 
                    str(file_manager.numpackets) + " packet(s) sent"
                    )
            pass

        pass