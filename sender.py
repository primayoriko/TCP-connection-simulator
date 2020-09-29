import socket
import sys
import time
from filemanager import FileManager
from packet import Packet

HOST = '127.0.0.1'
PORT = 1338
MAX_SEG_SIZE = 32774
TIMEOUT = 3

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
                            # data=format(
                            #                 data_chunks[i], 
                            #                 '#0{padding}b'
                            #                     .format(padding=MAX_SEG_SIZE+2)
                            #             )[2:]
                        )
        packet.checksum = Packet.checksum(packet)
        packets.append(packet)

    return packets

def run():
    # Get parameter from command-line
    receiver_hosts = sys.argv[1].split(',')
    receiver_port = int(sys.argv[2])
    file_path = sys.argv[3]

    file_manager = FileManager()
    file_manager.addFile(file_path)
    packets = create_packets(file_manager.data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    # sock.bind((HOST, PORT))
    
    # print(receiver_hosts)
    # print(receiver_port)
    # print(file_path)
    # print(f'File input checksum: 0x{file_manager.checksum:04x}')
    # print(file_manager.numpackets)

    # Sent packets one by one per receiver 
    for receiver_host in receiver_hosts:
        success = 0
        arr_succeed = [False for i in range(file_manager.numpackets)]

        # Loop until all data sent
        while(success < file_manager.numpackets):
            for i in range(file_manager.numpackets):
                if(not arr_succeed[i]):
                    sent = False

                    # Looping packet until successfully sent
                    while(not sent):
                        sock.sendto(Packet.to_bytes(packets[i]),
                                    (receiver_host, receiver_port)
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
                    print("Status : " + str(success) + "/" + 
                            str(file_manager.numpackets) + " packet(s) sent"
                        )
                    # print("Details : " +str(arr_succeed))
        pass

        if(success == file_manager.numpackets):
            print("{file} successfully sent to {host}:{port}!"
                    .format(file=file_path, host=receiver_host, port=receiver_port) 
                )

if __name__ == '__main__':
    run()