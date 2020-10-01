import socket
import sys
from packet import Metadata, Packet, unpackPacket
from filemanager_sender import FileManagerSender

HOST = '127.0.0.1'
PORT = 1338
MAX_SEG_SIZE = 32774
TIMEOUT = 0.5 # 0.5 secs

def create_packet(data_chunk, seqnum, isFin):
    return Packet(
                    pack_type='DATA' if not isFin 
                                        else 'FIN',
                    length=len(data_chunk),
                    seqnum=seqnum,
                    data=data_chunk
                )

def run():
    # Get parameter from command-line
    receiver_hosts = sys.argv[1].split(',')
    receiver_port = int(sys.argv[2])
    file_path = sys.argv[3]
    use_metadata = False
    use_multithreading = False
    if len(sys.argv) > 4:
        if sys.argv[4] == '1':
            use_metadata = True
        elif sys.argv[4] == '2':
            use_multithreading = True
        elif sys.argv[4] == '3':
            use_metadata = True
            use_multithreading = True

    file_manager = FileManagerSender(file_path)
    packets_num = file_manager.total_chunk

    finished, receivers_num = 0, len(receiver_hosts)
    succ_packets_nums = [0 for i in range(receivers_num)]
    if use_metadata:
        succ_metadata = [False for i in range(receivers_num)]
        metadata = Metadata(file_manager.metadata['name'], file_manager.metadata['size'])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    while(finished < receivers_num):
        for num in range(receivers_num):
            curr_num = succ_packets_nums[num]
            if(curr_num == packets_num):
                continue
            
            packet = create_packet(file_manager.getChunk(curr_num), 
                                    curr_num, curr_num == packets_num - 1)
            if use_metadata and not succ_metadata[num]:
                sock.sendto(Metadata.to_bytes(metadata),
                        (receiver_hosts[num], receiver_port)
                    )
            else:
                sock.sendto(Packet.to_bytes(packet),
                            (receiver_hosts[num], receiver_port)
                        )
            try:
                data_response, addr = sock.recvfrom(MAX_SEG_SIZE)
                response_packet = Packet.from_bytes(data_response)
                if use_metadata and not succ_metadata[num]:
                    print(f"Metadata sent successfully to {receiver_hosts[num]}:{receiver_port}!")
                    succ_metadata[num] = True
                elif(
                    (packet.is_data() and response_packet.is_ack() and curr_num == response_packet.seqnum)
                    or
                    (packet.is_fin() and response_packet.is_finack() and curr_num == response_packet.seqnum)
                ):
                    succ_packets_nums[num] += 1
                    print(
                            "Packet {i} sent successfully to {host}:{port}!"
                                .format(i=curr_num, host=receiver_hosts[num], port=receiver_port)
                        )

            except socket.timeout:
                if use_metadata and not succ_metadata[num]:
                    print(f"Metadata failed to sent to {receiver_hosts[num]}:{receiver_port}!")
                else:
                    print(
                            "Packet {i} failed to sent to {host}:{port}!"
                                .format(i=curr_num, host=receiver_hosts[num], port=receiver_port)
                        )
                pass
            
            finally:
                print(
                        "{0} status : {1}/{2} packet(s) sent"
                            .format(receiver_hosts[num], succ_packets_nums[num], packets_num)
                    )
                if(succ_packets_nums[num] == packets_num):
                    finished += 1
                    print(
                        "Transfer to {host} finished!"
                            .format(host = receiver_hosts[num])
                    )

    if(finished == receivers_num):
        print("All targets receive file successfully!!")

if __name__ == '__main__':
    run()