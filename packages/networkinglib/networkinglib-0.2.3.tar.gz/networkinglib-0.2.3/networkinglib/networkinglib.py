import tcp_client, udp_client

class tcp:
    def __init__(self, address, port):
        address, port = format_address(address, port)
        self.socket = tcp_client.connect(address, port)

    def receive(self):
        # receive tcp packets
        return tcp_client.receive(self.socket)

    def send(self, message):
        # send tcp packets
        return tcp_client.send(message, self.socket)

    def close(self):
        # close socket
        return tcp_client.close(self.socket)


    @classmethod
    def connect(address, port):
        return tcp(address, port)



class udp:
    def __init__(self):
        self.socket = udp_client.open()

    def send(self, msg, address, port=False):
        # send udp packets
        address, port = format_address(address, port)
        udp_client.send(msg, address, port, self.socket)

    def receive(self):
        # receive udp packets
        return udp_client.receive(self.socket)

    def close(self):
        # close socket
        udp_client.close(self.socket)


    @classmethod
    def open(self):
        return udp()



def format_address(address, port):
    # C implementations need IP addresses and cannot work with hostnames
    address.replace('localhost', '127.0.0.1')
    if not port:
        address, port = address.split(':')
    return address, port