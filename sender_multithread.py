import socket
import sys
import time
import threading
from _thread import *
from filemanager import FileManager
from packet import Packet

HOST = '127.0.0.1'
PORT = 1338
MAX_SEG_SIZE = 32774
TIMEOUT = 3

send_lock = threading.Lock()
print_lock = threading.Lock()

def get_time_millis():
    return int(round(time.time() * 1000))

# Packaging sequence of data into sequence of packets
def create_packets(data_chunks):
    packets, total_chunks = [], len(data_chunks)
    for num in range(total_chunks):
        packet = Packet(
                            pack_type='DATA' if num != total_chunks - 1
                                                else 'FIN',
                            length=len(data_chunks[num]),
                            seqnum=num,
                            data=data_chunks[num]
                        )
        packet.checksum = Packet.checksum(packet)
        packets.append(packet)

    return packets

def send_packet_threaded():
    return 0

def reciever_threaded(sock, reciever_addr, reciever_port, packets):
    numpackets, success = len(packets), 0
    arr_succeed = [False for i in range(numpackets)]

    # Loop until all data sent
    while(success < numpackets):
        for i in range(numpackets):
            if(not arr_succeed[i]):
                sent = False

                # Looping packet until successfully sent
                while(not sent):
                    sock.sendto(Packet.to_bytes(packets[i]),
                                (reciever_addr, reciever_port)
                            )
                    try:
                        data_response, addr = sock.recvfrom(MAX_SEG_SIZE)
                        response_packet = Packet.from_bytes(data_response)
                        if(
                            (packets[i].is_data() and response_packet.is_ack())
                            or
                            (packets[i].is_fin() and response_packet.is_finack())
                        ):
                            sent = True
                            print("Packet {0} successfully sended!".format(i))
                    except socket.timeout:
                        print("Timeout reached, retrying....")

                arr_succeed[i] = sent
                success += 1 
                print(
                        "Status : {0}/{1} packet(s) sent"
                            .format(success, numpackets)
                    )
                print("Details : " +str(arr_succeed))
    
    if(success == numpackets):
        print("File successfully sent to {host}:{port}!"
                .format(host=reciever_addr, port=reciever_port) 
            )

def run():
    # Get parameter from command-line
    reciever_hosts = sys.argv[1].split(',')
    reciever_port = int(sys.argv[2])
    file_path = sys.argv[3]

    file_manager = FileManager()
    file_manager.addFile(file_path)
    packets = create_packets(file_manager.data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    # sock.bind((HOST, PORT))
    
    # print(reciever_hosts)
    # print(reciever_port)
    # print(file_path)
    # print(f'File input checksum: 0x{file_manager.checksum:04x}')
    # print(file_manager.numpackets)

    # Sent packets one by one per reciever 
    threads = [
                threading.Thread(
                                    target=reciever_threaded,
                                    args=(sock, reciever_addr, reciever_port, packets,)
                                )
                for reciever_addr in reciever_hosts
            ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    run()