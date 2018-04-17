import time
import socket
from scapy.all import *
# https://scapy.readthedocs.io/en/latest/installation.html#installing-scapy-v2-x
from multiprocessing.pool import ThreadPool as Pool

TIMEOUT = 10
hostname = "google.com"
# port = 33434 #port 33434-33523 is used for traceroute

# serial
print("Serial")
last_visited = ""
name = ""
for i in range(1, 30):
    serial_pkt = IP(dst=hostname, ttl=i) / ICMP()
    # Send the packet and get a reply. sr1 is usefule for pinging an ip
    time_before = time.time()
    reply = sr1(serial_pkt, verbose=0, timeout=TIMEOUT, retry=3)
    time_after = time.time()
    if reply is None:
        # No reply =(
        print("{index}: <ICMP timeout>".format(index=i))
        # break
    elif reply.src == last_visited:  # Host has been reached

        print "Done!"
        break
    else:  # Still tracing the route
        # save the last visited to compare later
        last_visited = reply.src
        # get host name, if no name use <No DNS entry>
        try:
            h_name = socket.gethostbyaddr(reply.src)
            name = h_name[0]
        except socket.error as e:
            name = "<No DNS entry>"
        # get time
        total_time = time_after - time_before
        # print
        print "{index}: {host_name} {ipaddress} {time} ms".format(index=i, host_name=name, ipaddress=reply.src,
                                                                  time=total_time)


#parallel
print("Parallel")

def send_packet(i):
    last_visited = ""
    serial_pkt = IP(dst=hostname, ttl=i) / ICMP()
    # Send the packet and get a reply. sr1 is usefule for pinging an ip
    time_before = time.time()
    reply = sr1(serial_pkt, verbose=0, timeout=TIMEOUT, retry=3)
    time_after = time.time()
    if reply is None:
        # No reply =(
        print("{index}: <ICMP timeout>".format(index=i))
        # break
    elif reply.src == last_visited:  # Host has been reached

        print "Done!"
    else:  # Still tracing the route
        # save the last visited to compare later
        last_visited = reply.src
        # get host name, if no name use <No DNS entry>
        try:
            h_name = socket.gethostbyaddr(reply.src)
            name = h_name[0]
        except socket.error as e:
            name = "<No DNS entry>"
        # get time
        total_time = time_after - time_before
        # print
        print "{index}: {host_name} {ipaddress} {time} ms".format(index=i, host_name=name, ipaddress=reply.src,
                                                                  time=total_time)

def worker(index):
    try:
        # print("Sending packet")
        send_packet(i)
    except:
        print("Error with sending packet")

pool = Pool(30)

print("starting for loop")
for i in range(1,30):
    # print("inside for loop")
    pool.apply_async(worker(i))

pool.close()
pool.join()