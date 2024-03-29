import socket
import sys
import threading
from _thread import *
from filemanager import FileManager
from packet import Packet

HOST = '127.0.0.1'
PORT = 1338
MAX_SEG_SIZE = 32774
TIMEOUT = 0.5 # in seconds

filemanager_lock = threading.Lock()

def create_packet(data_chunk, seqnum, isFin):
    return Packet(
                    pack_type='DATA' if not isFin 
                                        else 'FIN',
                    length=len(data_chunk),
                    seqnum=seqnum,
                    data=data_chunk
                )

def send_threaded(file_manager, reciever_addr, reciever_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    curr_num, packets_num = 0, file_manager.total_chunk

    while(curr_num < packets_num):
        sent = False
        filemanager_lock.acquire()
        packet = create_packet(
                        file_manager.getChunk(curr_num),
                        curr_num, 
                        curr_num == packets_num - 1
                    )
        filemanager_lock.release()

        while(not sent):
            sock.sendto(Packet.to_bytes(packet), (reciever_addr, reciever_port))
            try:
                data_response, addr = sock.recvfrom(MAX_SEG_SIZE)
                response_packet = Packet.from_bytes(data_response)
                if(
                    (packet.is_data() and response_packet.is_ack() 
                        and curr_num == response_packet.seqnum)
                    or
                    (packet.is_fin() and response_packet.is_finack() 
                        and curr_num == response_packet.seqnum)
                ):
                    print(f"Packet {curr_num} successfully sent to {reciever_addr}:{reciever_port}!")
                    sent = True
                    curr_num += 1
            except socket.timeout:
                print(f"Timeout to {reciever_addr}:{reciever_port} reached, retrying....")
            finally:
                print(
                        "Status : {0}/{1} packet(s) sent"
                            .format(curr_num, packets_num)
                    )
    
    if(curr_num == packets_num):
        print("File successfully sent to {host}:{port}!"
                .format(host=reciever_addr, port=reciever_port) 
            )

def run():
    import time
    # Get parameter from command-line
    reciever_hosts = sys.argv[1].split(',')
    reciever_port = int(sys.argv[2])
    file_path = sys.argv[3]

    file_manager = FileManager(file_path)

    # Sent packets one by one per reciever 
    threads = [
                threading.Thread(
                                    target=send_threaded,
                                    args=(file_manager, reciever_addr, reciever_port,)
                                )
                for reciever_addr in reciever_hosts
            ]

    for thread in threads:
        thread.start()
    start_time = time.perf_counter()
    for thread in threads:
        thread.join()
    end_time = time.perf_counter()

    print("All targets receive file successfully!!")
    print(f'Program finished sending file for {(end_time-start_time)*1000:.2f}ms')
if __name__ == '__main__':
    run()