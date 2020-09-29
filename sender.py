import socket
import sys
from filemanager import FileManager
from packet import Packet

HOST = '127.0.0.1'
PORT = 1338
MAX_SEG_SIZE = 32774
TIMEOUT = 3 # 3 secs

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

def run():
    # Get parameter from command-line
    receiver_hosts = sys.argv[1].split(',')
    receiver_port = int(sys.argv[2])
    file_path = sys.argv[3]

    file_manager = FileManager()
    file_manager.addFile(file_path)
    packets = create_packets(file_manager.data)
    packets_num = len(packets)

    finished, receivers_num = 0, len(receiver_hosts)
    succ_packets_nums = [0 for i in range(receivers_num)]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    # sock.bind((HOST, PORT))
    
    # print(receiver_hosts)
    # print(receiver_port)
    # print(file_path)
    # print(f'File input checksum: 0x{file_manager.checksum:04x}')
    # print(file_manager.numpackets)

    while(finished < receivers_num):
        for num in range(receivers_num):
            curr_num = succ_packets_nums[num]
            if(curr_num == packets_num):
                continue
            
            sock.sendto(Packet.to_bytes(packets[curr_num]),
                        (receiver_hosts[num], receiver_port)
                    )
            try:
                data_response, addr = sock.recvfrom(MAX_SEG_SIZE)
                response_packet = Packet.from_bytes(data_response)
                if(
                    (packets[curr_num].is_data() and response_packet.is_ack())
                    or
                    (packets[curr_num].is_fin() and response_packet.is_finack())
                ):
                    succ_packets_nums[num] += 1
                    print(
                            "Packet {i} sent successfully to {host}:{port}!"
                                .format(i=curr_num, host=receiver_hosts[num], port=receiver_port)
                        )

            except socket.timeout:
                print(
                        "Packet {i} failed to sent to {host}:{port}!"
                            .format(i=curr_num, host=receiver_hosts[num], port=receiver_port)
                    )
            
            finally:
                print(
                        "{0} status : {1}/{2} packet(s) sent"
                            .format(receiver_hosts[num], succ_packets_nums[num], packets_num)
                    )
                if(succ_packets_nums[num] == packets_num):
                    print(
                        "Transfer to {host} finished!"
                            .format(host = receiver_hosts[num])
                    )

    if(finished == packets_num):
        print("All file transfer succeed!!")

if __name__ == '__main__':
    run()