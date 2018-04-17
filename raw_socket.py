import socket
import select
import struct
import sys

# resources: https://docs.python.org/3/howto/sockets.html

# constants used in tcpsocket.py
BUF_SIZE = 512
TIMEOUT = 10  # timeout duration in select() in seconds


# Define class (instance variables and methods)
class Raw_Socket:

    # Constructor: create an object
    def __init__(self, host_name, port_number):
        #create send socket
        self.send_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM,
            proto=socket.IPPROTO_UDP
        )
        #create receive socket
        self.receive_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_RAW,
            proto=socket.IPPROTO_ICMP
        )
        # get ipaddress of host
        self.ip_address = socket.gethostbyname(host_name)
        self.port = port_number
        self.host = host_name

        #send the packet
        def send_packet(self, ttl, port):
            self.send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            #byte array = b''
            self.send_socket.sendto(b'', (self.ip_address, self.port))
            self.send_socket.close()

        #receive the reply
        def receive_reply(self):
            inputs = [self.send_socket, sys.stdin]
            outputs = []
            #GNU timeval structure
            receive_timeout = struct.pack("11", 5, 0)
            #set the receive timeout
            self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, TIMEOUT)
            ready = select.select(inputs, outputs, [], TIMEOUT)
            if ready[0] == []: #timeout
                print("Time out on ", self.host)
                return ""
            #else reader has data to read
            try:
                #get 512 bytes from the server
               address = self.receive_socket.recvfrom(BUF_SIZE)
              # address = address[0]
               try:
                   #get the host name
                   name = socket.gethostbyaddr(address)[0]
               except socket.error:
                   #if can't the host name, show the ipdaddress
                   name = address
            except socket.error as e:
                print("socket error in receive: {}".format(e))
                name = "socket error"

            self.receive_socket.close()
            return name;


