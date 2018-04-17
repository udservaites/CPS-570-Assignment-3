import socket
import sys


class TraceRoute(object):
    BADDR = "0.0.0.0"  # default bind address - (all IPs)
    PORT = 33434  # default port
    ICMP = socket.getprotobyname('icmp')
    UDP = socket.getprotobyname('udp')

    desternation = ""
    ttl = 0  # we inrecement this by one each time.

    # sockets
    reciever = None
    sender = None

    # finished?
    finished = False

    def __init__(self, desternation):
        self.desternation = socket.gethostbyname(desternation)

        self.reciever = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.ICMP)
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, self.UDP)

        # bind to reciever so we can listen for replies
        self.reciever.bind((self.BADDR, self.PORT))

    def next_server(self):
        """ Connects to next server 1 hop away from current server (i.e. server[ttl + 1]) """
        if self.finished:
            # we have nothing to do, just return
            return

        # first job increment the ttl on the socket
        self.ttl += 1
        self.sender.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)

        self.sender.sendto("", (self.desternation, self.PORT))
        current_server = self.reciever.recvfrom(512)[1][0]  # get 512 bytes from the reciever
        self.display(current_server)

        if current_server == self.desternation:
            self.finished = True

    def display(self, address):
        """ Gets the hostname (if we can) and displays """
        try:
            name = socket.gethostbyaddr(address)[0]
            print "%s) %s (%s)" % (self.ttl, name, address)
        except socket.error:
            # we couldn't - we'll just tell them the IP address
            print "%s) %s" % (self.ttl, address)

    def __del__(self):
        """ Be good and close our sockets """
        try:
            self.reciever.close()
        except socket.error:
            # already closed
            pass

        try:
            self.sender.close()
        except socket.error:
            # already closed
            pass


if __name__ == "__main__":
    # lets get the address from the commandline args
 #   if len(sys.argv) <= 1:
  #      # nothing been specified
   #     print "You need to give an address"
    #    print "%s <server>" % sys.argv[0]
     #   sys.exit()  # we can't do anything.

    tracert = TraceRoute("www.google.com")
    while not tracert.finished:
        tracert.next_server()