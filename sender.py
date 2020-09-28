import socket
import sys
import time
from filemanager import FileManager
# from packet import Packet

HOST = '127.0.0.1'
PORT = 1338
MAX_SEG_SIZE = 32774
TIMEOUT = 3

def get_time_millis():
    return int(round(time.time() * 1000))

def run():
    # Get parameter from command-line (*NEED TO BE FIXED*)
    file_path = sys.argv[1]
    targets = sys.argv[2:]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    sock.bind((HOST, PORT))
    
    print(file_path)
    print(targets)

    # Sent packets one by one per target 
    for target in targets:
        file_manager = FileManager()
        file_manager.addFile(file_path)
        success = 0
        arr_succeed = [False for i in range(file_manager.numpackets)]

        print(f'File input checksum: 0x{file_manager.checksum:04x}')
        print(file_manager.numpackets)

        # Loop until all data sent
        while(success < file_manager.numpackets):
            for i in range(file_manager.numpackets):
                if(not arr_succeed[i]):
                    sent = False
                    # s.connect((HOST, PORT))

                    # Looping packet until successfully sent
                    while(not sent):
                        s.sendto(Packet.to_bytes(file_manager.data[i]),
                                    (HOST, PORT)
                                )
                        try:
                            conn, addr = socket.recvfrom(MAX_SEG_SIZE)
                            packet = Packet.from_bytes(data)
                            if(packet.is_ack()):
                                sent = True
                                break
                        except socket.Timeout:
                            pass

                    arr_succeed[i] = sent
                    success += 1 

            print("Status : " + str(success) + "/" + 
                    str(file_manager.numpackets) + " packet(s) sent"
                )
            print("Details : " +str(arr_succeed))
        pass

if __name__ == '__main__':
    run()