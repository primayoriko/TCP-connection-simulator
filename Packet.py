# Packet data structure

class Packet:
    def __init__(self, data_type, seq_num, data):
        self.data_type = data_type
        self.seq_num = seq_num
        self.data = data

        total = str(data_type) + str(seq_num) + str(data)
        self.checksum = 0

        for i in range(total.length, ):
            pass
