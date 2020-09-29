import socket
import sys
from packet import Packet, Metadata, unpackPacket
from filemanager import FileManager

PORT = int(sys.argv[1])
ADDRESS = "127.0.0.1"
MAX_SEG_SIZE = 32774

def same_checksum(packet):
    return Packet.checksum(packet) == packet.checksum

def generate_ack(seqnum, fin_ack=False):
    if not fin_ack:
        pkt_type = 'ACK'
    else:
        pkt_type = 'FIN-ACK'
    
    ack_pkt = Packet(pkt_type, 0, seqnum)
    return Packet.to_bytes(ack_pkt)

def run():
    # Init socket
    sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_listen.bind(('', PORT))
    print("[+] Listening on %s port %d" % (ADDRESS, PORT))
    
    # Resources to receive data
    file_manager = FileManager()
    prev_seqnum = -1

    # Listen loop
    while True:
        data, addr = sock_listen.recvfrom(MAX_SEG_SIZE)
        pkt = unpackPacket(data)
        if isinstance(pkt, Metadata):
            print(f"[-1] Metadata received! file_name={pkt.file_name} & file_size={pkt.file_size}")
            file_manager.addMetadata(pkt.file_name, pkt.file_size)
            sock_listen.sendto(
                    generate_ack(0), addr
                )
            continue
        print("[%d] Hit!" % pkt.seqnum)


        # If pkt is the next in sequence and same checksum, append and send ack
        if pkt.seqnum == prev_seqnum + 1 and same_checksum(pkt):
            
            # Append to received packet array
            file_manager.addData(pkt.seqnum, pkt.data)
            prev_seqnum += 1

            if pkt.is_fin():
                # Send fin-ack packet
                sock_listen.sendto(
                    generate_ack(prev_seqnum, True), addr
                )
                # End loop
                break
            else:
                sock_listen.sendto(
                    generate_ack(prev_seqnum), addr
                )

    
    # FileManager piece the data together here, save to ./out/downloaded
    file_manager.writeFile()


if __name__ == '__main__':
    run()