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

def create_packets(data_chunks):
    packets, num = [], 0
    for chunk in data_chunks:
        num += 1
        packet = Packet(
                            pack_type='DATA',
                            length=len(chunk),
                            seqnum=num,
                            data=chunk
                            # data=format(
                            #                 chunk, 
                            #                 '#0{padding}b'
                            #                     .format(padding=MAX_SEG_SIZE+2)
                            #             )[2:]
                        )
        packet.checksum = Packet.checksum(packet)
        packets.append(packet)

    return packets

def run():
    # Get parameter from command-line (*NEED TO BE FIXED*)
    hosts_target = sys.argv[1].split(',')
    port_target = int(sys.argv[2])
    file_path = sys.argv[3]

    file_manager = FileManager()
    file_manager.addFile(file_path)
    packets = create_packets(file_manager.data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    sock.bind((HOST, PORT))
    
    print(hosts_target)
    print(port_target)
    print(file_path)

    print(f'File input checksum: 0x{file_manager.checksum:04x}')
    print(file_manager.numpackets)

    # Sent packets one by one per target 
    for target in hosts_target:
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
                                    (target, port_target)
                                )
                        try:
                            data, addr = sock.recvfrom(MAX_SEG_SIZE)
                            packet = Packet.from_bytes(data)
                            if(packet.is_ack()):
                                sent = True
                                break
                        except socket.timeout:
                            print("Timeout reached, retrying....")

                    arr_succeed[i] = sent
                    success += 1 
                    print("Status : " + str(success) + "/" + 
                            str(file_manager.numpackets) + " packet(s) sent"
                        )
                    print("Details : " +str(arr_succeed))
        pass

        if(success == file_manager.numpackets):
            fin_packet = Packet(pack_type='FIN')
            while(not sent):
                sock.sendto(Packet.to_bytes(fin_packet),
                            (target, port_target)
                        )
                try:
                    data, addr = sock.recvfrom(MAX_SEG_SIZE)
                    packet = Packet.from_bytes(data)
                    if(packet.is_finack()):
                        sent = True
                        break
                except socket.timeout:
                    print("Timeout reached, retrying....")
                    
            if(sent):
                print("File successfully sent to {host}:{port}!"
                        .format(host=target, port=port_target) 
                    )

if __name__ == '__main__':
    run()